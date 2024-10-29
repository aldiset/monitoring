from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.database import Base

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    framework = Column(String)
    specification = Column(String)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
