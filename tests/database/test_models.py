# tests/database/test_models.py

import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the models
from database.models import Base, SomeModel

# In-memory SQLite for testing purposes
DATABASE_URL = "sqlite:///:memory:"

# Create an engine and a testing session
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Provide a database session fixture for testing."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_some_model(db_session):
    """Test functionality of SomeModel."""
    # Add a sample record
    new_record = SomeModel(name="Test Item", description="Test Description")
    db_session.add(new_record)
    db_session.commit()

    # Query the record
    result = db_session.query(SomeModel).filter_by(name="Test Item").first()
    assert result is not None
    assert result.name == "Test Item"
    assert result.description == "Test Description"
