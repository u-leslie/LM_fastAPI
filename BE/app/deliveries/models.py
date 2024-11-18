from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    delivery_status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))

    shipment = relationship("Shipment")
    driver = relationship("Driver")
