from pydantic import BaseModel

class DeliveryCreate(BaseModel):
    date: str
    delivery_status: str
    owner_id: int
    shipment_id: int
    driver_id: int
