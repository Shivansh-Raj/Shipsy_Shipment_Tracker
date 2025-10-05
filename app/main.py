from fastapi import FastAPI
from app.routers import auth

from app.database import Base, engine
from app.models import user 

from fastapi.middleware.cors import CORSMiddleware

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


app = FastAPI(title="Shipment Tracker API")

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Shipment Tracker API is running 🚚"}
