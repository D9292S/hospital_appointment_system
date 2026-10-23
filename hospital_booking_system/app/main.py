from fastapi import FastAPI
from app.database import Base, engine
from app.routers import doctors, appointments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Appointment Booking API",
    description="A debugging challenge for beginner FastAPI developers.",
    version="1.0.0",
)

app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/")
def health_check():
    return {"message": "Hospital Appointment Booking API is running"}
