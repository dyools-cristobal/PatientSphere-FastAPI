from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Optional 
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

class ClinicBase(BaseModel):
    name: str
    address: str
    phone_number: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class PatientBase(BaseModel):

    dr_id: int
    first_name: str
    middle_name: str
    last_name: str
    photo_link: str
    gender: int
    age_of_gestation: Decimal
    birth_weight: Decimal
    birth_length: Decimal
    head_circumference: Decimal
    chest_circumference: Decimal
    abdomen_circumference: Decimal
    newborn_screening: Optional[str]
    blood_type: Optional[str]
    known_allergies: Optional[str]
    perinatal_history: Optional[str]
    date_of_birth: str
    time_of_birth: str
    mother_first_name: Optional[str]
    mother_last_name: Optional[str]
    mother_age: Optional[int]
    mother_occupation: Optional[str]
    mother_contact_number: Optional[str]
    mother_email_address: Optional[str]
    father_first_name: Optional[str]
    father_last_name: Optional[str]
    father_age: Optional[int]
    father_occupation: Optional[str]
    father_contact_number: Optional[str]
    father_email_address: Optional[str]
    home_address: Optional[str]
    home_phone_number: Optional[str]



#create patient
@router.post("/patients/", status_code=status.HTTP_201_CREATED)
async def create_patient(patient:PatientBase, db: db_dependency):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()

# update patient
@router.put("/patients/{patient_id}", status_code=status.HTTP_200_OK)
async def update_patient(patient_id: int, patient: PatientBase, db: db_dependency):
    # Retrieve the patient from the database
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    
    # Check if the patient exists
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update patient attributes
    for attr, value in patient.dict().items():
        setattr(db_patient, attr, value)
    
    # Commit changes to the database
    db.commit()
    
    return db_patient

# get all patients by dr_id
@router.get("/all_dr_patients/{dr_id}", status_code=status.HTTP_200_OK)
async def read_user(dr_id: int, db: db_dependency):
    patients = db.query(models.Patient).filter(models.Patient.dr_id == dr_id).all()
    if patients is None:
        raise HTTPException(status_code=404, detail='No patients found')
    return patients

# get dr patient by id
@router.get("/patients/{dr_id}/{patient_id}", status_code=status.HTTP_200_OK)
async def read_user(dr_id: int, patient_id, db: db_dependency):
    patients = db.query(models.Patient).filter((models.Patient.dr_id == dr_id) & (models.Patient.id == patient_id)).first()
    if patients is None:
        raise HTTPException(status_code=404, detail='No patients found')
    return patients