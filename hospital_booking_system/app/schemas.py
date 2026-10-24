from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DoctorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    specialization: str = Field(min_length=2, max_length=100)
      
    consultation_fee: float = Field(ge=0)



class DoctorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    specialization: str
    consultation_fee: float


class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime


class AppointmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    status: str
    fee: float


class AppointmentReschedule(BaseModel):
    appointment_time: datetime
