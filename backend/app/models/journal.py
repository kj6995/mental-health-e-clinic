from datetime import datetime
import uuid
import json
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

def generate_uuid():
    return str(uuid.uuid4())

class Journal(Base):
    __tablename__ = "journals"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Using Text for longer content
    _tags = Column('tags', Text, nullable=False, default='[]')  # Store tags as JSON string
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to user
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="journals")

    @property
    def tags(self):
        """Convert JSON string to list when accessing tags"""
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        """Convert list to JSON string when setting tags"""
        self._tags = json.dumps(value)
