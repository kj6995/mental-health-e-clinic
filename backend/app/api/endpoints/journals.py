from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.api.deps import get_db
from app.models.journal import Journal
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

class JournalBase(BaseModel):
    title: str
    content: str
    tags: List[str]

class JournalCreate(JournalBase):
    pass

class JournalUpdate(JournalBase):
    pass

class JournalResponse(JournalBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class PaginatedJournalResponse(BaseModel):
    page: int
    per_page: int
    total_pages: int
    total_records: int
    data: List[JournalResponse]

@router.get("/", response_model=PaginatedJournalResponse)
async def get_journals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(Journal).filter(Journal.user_id == current_user.id)

    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Journal.title.ilike(search_term),
                Journal._tags.ilike(f"%{search}%"),
                Journal.content.ilike(search_term)
            )
        )

    # Apply date filters if provided
    if start_date:
        query = query.filter(Journal.updatedAt >= start_date)
    if end_date:
        query = query.filter(Journal.updatedAt <= end_date)

    # Get total count for pagination
    total_records = query.count()
    total_pages = (total_records + per_page - 1) // per_page

    # Apply pagination and ordering
    query = query.order_by(desc(Journal.updatedAt))\
                .offset((page - 1) * per_page)\
                .limit(per_page)

    journals = query.all()

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_records": total_records,
        "data": journals
    }

@router.post("/", response_model=JournalResponse)
async def create_journal(
    journal: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_journal = Journal(
        user_id=current_user.id,
        title=journal.title,
        content=journal.content,
        tags=journal.tags
    )
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal

@router.get("/{journal_id}", response_model=JournalResponse)
async def get_journal(
    journal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.user_id == current_user.id
    ).first()
    
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    
    return journal

@router.put("/{journal_id}", response_model=JournalResponse)
async def update_journal(
    journal_id: str,
    journal_update: JournalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.user_id == current_user.id
    ).first()
    
    if not db_journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    
    db_journal.title = journal_update.title
    db_journal.content = journal_update.content
    db_journal.tags = journal_update.tags
    db_journal.updatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(db_journal)
    return db_journal

@router.delete("/{journal_id}")
async def delete_journal(
    journal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.user_id == current_user.id
    ).first()
    
    if not db_journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    
    db.delete(db_journal)
    db.commit()
    return {"message": "Journal deleted successfully"}
