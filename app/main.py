from fastapi import FastAPI

app = FastAPI(title="Shipment Tracker API")

@app.get("/")
def root():
    return {"message": "Shipment Tracker API is running 🚚==="}
