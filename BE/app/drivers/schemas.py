from pydantic import BaseModel

class DriverCreate(BaseModel):
    name: str
    vehicle_number: str
    phone_number: str
    is_available: bool
