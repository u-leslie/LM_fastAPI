from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from app.accounts.routes import router as accounts_router
from app.drivers.routes import router as drivers_router
from app.shipments.routes import router as shipments_router
from app.deliveries.routes import router as deliveries_router

app = FastAPI(
    title="Logistics Management System",  
    description=(
        "This is the API documentation for the Logistics Management System. "
        "It provides endpoints for managing deliveries, shipments, drivers, and more."
    ),  
    version="1.0.0", 
    contact={
        "name": "UHIRIWE Anne Leslie",
        "email": "anneuhiriwe@gmail.com",
    },
)


security = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]  
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include your routers
app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
app.include_router(drivers_router, prefix="/drivers", tags=["Drivers"])
app.include_router(shipments_router, prefix="/shipments", tags=["Shipments"])
app.include_router(deliveries_router, prefix="/deliveries", tags=["Deliveries"])
