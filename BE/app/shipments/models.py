from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.drivers.models import Driver

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    status = Column(String, default="pending")
    driver_id = Column(Integer, ForeignKey("drivers.id"))

    driver = relationship("Driver")
