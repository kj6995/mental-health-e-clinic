from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.therapist import Therapist, Specialization
from app.schemas.therapist import TherapistCreate, TherapistUpdate

def get_therapist(db: Session, therapist_id: int) -> Optional[Therapist]:
    return db.query(Therapist).options(joinedload(Therapist.specializations)).filter(Therapist.id == therapist_id).first()

def get_therapists(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[float] = None
) -> List[Therapist]:
    query = db.query(Therapist).options(joinedload(Therapist.specializations))
    
    if search:
        query = query.filter(
            Therapist.name.ilike(f"%{search}%") | 
            Therapist.description.ilike(f"%{search}%")
        )
    
    if category:
        query = query.filter(Therapist.category == category)
    
    if min_rating is not None:
        query = query.filter(Therapist.rating >= min_rating)
    
    return query.offset(skip).limit(limit).all()

def get_total_therapists(
    db: Session,
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[float] = None
) -> int:
    query = db.query(Therapist)
    
    if search:
        query = query.filter(
            Therapist.name.ilike(f"%{search}%") | 
            Therapist.description.ilike(f"%{search}%")
        )
    
    if category:
        query = query.filter(Therapist.category == category)
    
    if min_rating is not None:
        query = query.filter(Therapist.rating >= min_rating)
    
    return query.count()

def get_categories(db: Session) -> List[str]:
    return [category[0] for category in db.query(Therapist.category).distinct().all()]

def create_therapist(db: Session, therapist: TherapistCreate) -> Therapist:
    # Create specializations first
    specializations = []
    for spec_name in therapist.specialization:
        spec = db.query(Specialization).filter(Specialization.name == spec_name).first()
        if not spec:
            spec = Specialization(name=spec_name)
        specializations.append(spec)
    
    # Create therapist
    db_therapist = Therapist(
        name=therapist.name,
        category=therapist.category,
        qualification=therapist.qualification,
        experience=therapist.experience,
        description=therapist.description,
        rating=therapist.rating,
        specializations=specializations
    )
    
    db.add(db_therapist)
    db.commit()
    db.refresh(db_therapist)
    return db_therapist

def update_therapist(
    db: Session, 
    therapist_id: int, 
    therapist_update: TherapistUpdate
) -> Optional[Therapist]:
    db_therapist = get_therapist(db, therapist_id)
    if not db_therapist:
        return None
        
    update_data = therapist_update.model_dump(exclude_unset=True)
    
    if "specialization" in update_data:
        specializations = []
        for spec_name in update_data["specialization"]:
            spec = db.query(Specialization).filter(Specialization.name == spec_name).first()
            if not spec:
                spec = Specialization(name=spec_name)
            specializations.append(spec)
        db_therapist.specializations = specializations
        del update_data["specialization"]
    
    for field, value in update_data.items():
        setattr(db_therapist, field, value)
    
    db.commit()
    db.refresh(db_therapist)
    return db_therapist

def delete_therapist(db: Session, therapist_id: int) -> bool:
    therapist = get_therapist(db, therapist_id)
    if not therapist:
        return False
    db.delete(therapist)
    db.commit()
    return True
