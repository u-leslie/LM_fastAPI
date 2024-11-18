from pydantic import BaseModel
from typing import Optional

class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    status: Optional[str] = "pending"
    driver_id: int
