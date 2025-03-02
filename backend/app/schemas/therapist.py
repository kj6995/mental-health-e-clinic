from typing import List, Optional
from pydantic import BaseModel, Field

class TherapistBase(BaseModel):
    name: str = Field(..., example="Shaily Tandon")
    category: str = Field(..., example="Trauma Therapist")
    qualification: str = Field(..., example="MS (Psychology)")
    experience: str = Field(..., example="15 years")
    description: str = Field(..., example="Shaily Tandon helps you in processing, healing, and reclaiming your strength after difficult experiences.")
    rating: float = Field(..., example=4.8)
    specialization: List[str] = Field(default_factory=list, example=["PTSD", "Trauma Counselling", "CBT"])

class SpecializationBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class TherapistCreate(TherapistBase):
    pass

class TherapistUpdate(TherapistBase):
    name: Optional[str] = None
    category: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    specialization: Optional[List[str]] = None

class Therapist(TherapistBase):
    id: int
    specialization: List[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # Convert SQLAlchemy model instance to Pydantic model
        if obj.specializations:
            # Extract specialization names from the relationship
            obj.__dict__['specialization'] = [s.name for s in obj.specializations]
        return super().from_orm(obj)

class TherapistPagination(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[Therapist]

    class Config:
        from_attributes = True
