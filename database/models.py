# database/models.py

from sqlalchemy.orm import declarative_base  # Updated import path
from sqlalchemy import Column, Integer, String

# Create the base class for all SQLAlchemy models
Base = declarative_base()

# Define an example model
class SomeModel(Base):
    __tablename__ = "some_model"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
