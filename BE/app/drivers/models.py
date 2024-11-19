from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    vehicle_number = Column(String)
    phone_number = Column(String)
    is_available = Column(Boolean, default=True)
    shipments = relationship("Shipment", back_populates="driver")
