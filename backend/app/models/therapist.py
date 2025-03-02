from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Association table for therapist-specialization many-to-many relationship
therapist_specialization = Table(
    'therapist_specialization',
    Base.metadata,
    Column('therapist_id', Integer, ForeignKey('therapists.id')),
    Column('specialization_id', Integer, ForeignKey('specializations.id'))
)

class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    therapists = relationship(
        "Therapist",
        secondary=therapist_specialization,
        back_populates="specializations"
    )

class Therapist(Base):
    __tablename__ = "therapists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    qualification = Column(String)
    experience = Column(String)
    description = Column(String)
    rating = Column(Float)
    
    specializations = relationship(
        "Specialization",
        secondary=therapist_specialization,
        back_populates="therapists"
    )
