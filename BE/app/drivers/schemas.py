from pydantic import BaseModel
from typing import Optional

class DriverBase(BaseModel):
    name: str
    vehicle_number: str
    phone_number: str
    is_available: Optional[bool] = True

class DriverCreate(DriverBase):
    pass

class DriverUpdate(BaseModel):
    name: Optional[str]
    vehicle_number: Optional[str]
    phone_number: Optional[str]
    is_available: Optional[bool]

class Driver(DriverBase):
    id: int

    class Config:
        orm_mode = True
