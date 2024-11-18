from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    vehicle_number = Column(String)
    phone_number = Column(String)
    is_available = Column(Boolean, default=True)
