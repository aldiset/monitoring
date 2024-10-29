from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import model
from datetime import datetime


# Database configuration
DATABASE_URL = "sqlite:///./data.db"  # Using SQLite for simplicity
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create database tables based on SQLAlchemy models."""
    model.Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

def initialize_data():
    """Initialize database with some data."""
    db = SessionLocal()
    try:
        # Example data
        data1 = model.Data(
            type="time",
            framework_name="FastAPI",
            specification="High Performance",
            result=[{"name": "response_time", "value": "0.1"}],
            created_at=datetime.now()
        )
        data2 = model.Data(
            type="cpu",
            framework_name="Django",
            specification="Multi-threading",
            result=[{"name": "cpu_usage", "value": "50"}],
            created_at=datetime.now()
        )

        # Add to session and commit
        db.add(data1)
        db.add(data2)
        db.commit()
        print("Data initialized successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    initialize_data()
