from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import model

DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    model.Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
if __name__ == "__main__":
    create_tables()
