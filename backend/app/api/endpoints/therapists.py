from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud import therapist as therapist_crud
from app.schemas.therapist import Therapist, TherapistCreate, TherapistUpdate, TherapistPagination
from app.api.deps import get_db

router = APIRouter()

@router.get("", response_model=TherapistPagination)
def get_therapists(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5)
):
    skip = (page - 1) * per_page
    therapists = therapist_crud.get_therapists(
        db,
        skip=skip,
        limit=per_page,
        search=search,
        category=category,
        min_rating=min_rating
    )
    total = therapist_crud.get_total_therapists(
        db,
        search=search,
        category=category,
        min_rating=min_rating
    )

    # Convert therapists to list of dictionaries with specialization names
    therapist_list = []
    for t in therapists:
        therapist_dict = {
            "id": t.id,
            "name": t.name,
            "category": t.category,
            "qualification": t.qualification,
            "experience": t.experience,
            "description": t.description,
            "rating": t.rating,
            "specialization": [s.name for s in t.specializations] if t.specializations else []
        }
        therapist_list.append(therapist_dict)

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "items": therapist_list
    }

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    return therapist_crud.get_categories(db)

@router.get("/{therapist_id}", response_model=Therapist)
def get_therapist(therapist_id: int, db: Session = Depends(get_db)):
    therapist = therapist_crud.get_therapist(db, therapist_id)
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist

@router.post("", response_model=Therapist)
def create_therapist(therapist: TherapistCreate, db: Session = Depends(get_db)):
    return therapist_crud.create_therapist(db, therapist)

@router.put("/{therapist_id}", response_model=Therapist)
def update_therapist(
    therapist_id: int,
    therapist_update: TherapistUpdate,
    db: Session = Depends(get_db)
):
    therapist = therapist_crud.update_therapist(db, therapist_id, therapist_update)
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist

@router.delete("/{therapist_id}")
def delete_therapist(therapist_id: int, db: Session = Depends(get_db)):
    if not therapist_crud.delete_therapist(db, therapist_id):
        raise HTTPException(status_code=404, detail="Therapist not found")
    return {"message": "Therapist deleted successfully"}
