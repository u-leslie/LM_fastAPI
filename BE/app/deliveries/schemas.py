from pydantic import BaseModel
from datetime import date
from typing import Optional


class DriverBase(BaseModel):
    id:int
    name: str
    phone_number: str
    vehicle_number: str


class Driver(DriverBase):
    id: int

    class Config:
        orm_mode = True


class ShipmentBase(BaseModel):
    origin: str
    destination: str
    status: str


class Shipment(ShipmentBase):
    id: int

    class Config:
        orm_mode = True


class DeliveryBase(BaseModel):
    date: date
    delivery_status: str
    owner_id: int
    shipment_id: int
    driver_id: int


class DeliveryCreate(DeliveryBase):
    pass


class Delivery(DeliveryBase):
    id: int
    shipment: Optional[Shipment] = None
    driver: Optional[Driver] = None

    class Config:
        orm_mode = True
