from fastapi import FastAPI
from app.accounts.routes import router as accounts_router
from app.drivers.routes import router as drivers_router
from app.shipments.routes import router as shipments_router
from app.deliveries.routes import router as deliveries_router

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
app.include_router(drivers_router, prefix="/drivers", tags=["Drivers"])
app.include_router(shipments_router, prefix="/shipments", tags=["Shipments"])
app.include_router(deliveries_router, prefix="/deliveries", tags=["Deliveries"])
