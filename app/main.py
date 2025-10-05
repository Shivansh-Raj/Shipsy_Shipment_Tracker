from fastapi import FastAPI, Depends
from app.routers import auth

from app.database import Base, engine
from app.models import user, shipment
from app.routers import auth, shipment

from fastapi.middleware.cors import CORSMiddleware

# Initializes FASTAPI
app = FastAPI(title="Shipment Tracker API")


# Allow all origins 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creates a database if missing
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(shipment.router)

# Default Emdpoint
@app.get("/")
def root():
    return {"message": "Shipment Tracker API is running 🚚===="}

