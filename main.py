from datetime import date, time
from decimal import Decimal
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Optional 
from sqlalchemy import Date, Time
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str
    role_id: int
    clinic_id: int

class RoleBase(BaseModel):
    description: str

class ClinicBase(BaseModel):
    name: str
    address: str
    phone_number: str

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

class GrowthBase(BaseModel):
    patient_id: int
    date_taken: str
    height: Decimal
    weight: Decimal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# create user
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

# update user
@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    # Retrieve the user from the database
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Check if the user exists
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user attributes
    for attr, value in user.dict().items():
        setattr(db_user, attr, value)
    
    # Commit changes to the database
    db.commit()
    
    return db_user

# get user by id
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# get all patients by dr_id
@app.get("/all_dr_patients/{dr_id}", status_code=status.HTTP_200_OK)
async def read_user(dr_id: int, db: db_dependency):
    patients = db.query(models.Patient).filter(models.Patient.dr_id == dr_id).all()
    if patients is None:
        raise HTTPException(status_code=404, detail='No patients found')
    return patients

# get dr patient by id
@app.get("/patients/{dr_id}/{patient_id}", status_code=status.HTTP_200_OK)
async def read_user(dr_id: int, patient_id, db: db_dependency):
    patients = db.query(models.Patient).filter((models.Patient.dr_id == dr_id) & (models.Patient.id == patient_id)).first()
    if patients is None:
        raise HTTPException(status_code=404, detail='No patients found')
    return patients

#create patient
@app.post("/patients/", status_code=status.HTTP_201_CREATED)
async def create_patient(patient:PatientBase, db: db_dependency):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()

# update patient
@app.put("/patients/{patient_id}", status_code=status.HTTP_200_OK)
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

#create clinic
@app.post("/clinics/", status_code=status.HTTP_201_CREATED)
async def create_clinic(clinic:ClinicBase, db: db_dependency):
    db_clinic = models.Clinic(**clinic.dict())
    db.add(db_clinic)
    db.commit()

#update clinic
@app.put("/clinics/{clinic_id}", status_code=status.HTTP_200_OK)
async def update_clinic(clinic_id: int, clinic: ClinicBase, db: db_dependency):
    db_clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not db_clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    # Update the clinic attributes
    for attr, value in clinic.dict().items():
        setattr(db_clinic, attr, value)
    
    db.commit()
    return db_clinic

# delete clinic
@app.delete("/clinics/{clinic_id}",status_code=status.HTTP_200_OK)
async def delete_clinic(clinic_id: int, db:db_dependency):
    db_clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if db_clinic is None:
        raise HTTPException(status_code=404, detail='Clinic not found')
    db.delete(db_clinic)
    db.commit()


#create role
@app.post("/roles/", status_code=status.HTTP_201_CREATED)
async def create_role(role:RoleBase, db: db_dependency):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()

# delete role
@app.delete("/roles/{role_id}",status_code=status.HTTP_200_OK)
async def delete_role(role_id: int, db:db_dependency):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail='Role not found')
    db.delete(db_role)
    db.commit()


# get all patients by dr_id
@app.get("/growth/{growth_id}", status_code=status.HTTP_200_OK)
async def read_user(patient_id: int, db: db_dependency):
    growth = db.query(models.Growth).filter(models.Growth.patient_id == patient_id).all()
    if growth is None:
        raise HTTPException(status_code=404, detail='No growth records found')
    return growth

#create growth
@app.post("/growth/", status_code=status.HTTP_201_CREATED)
async def create_growth(growth:GrowthBase, db: db_dependency):
    db_growth = models.Growth(**growth.dict())
    db.add(db_growth)
    db.commit()

#update growth
@app.put("/growth/{growth_id}", status_code=status.HTTP_200_OK)
async def update_growth(growth_id: int, growth: GrowthBase, db: db_dependency):
    db_growth = db.query(models.Growth).filter(models.Growth.id == growth_id).first()
    if not db_growth:
        raise HTTPException(status_code=404, detail="Growth record not found")
    
    # Update the clinic attributes
    for attr, value in growth.dict().items():
        setattr(db_growth, attr, value)
    
    db.commit()
    return db_growth

# delete growth
@app.delete("/growth/{growth_id}",status_code=status.HTTP_200_OK)
async def delete_growth(growth_id: int, db:db_dependency):
    db_growth = db.query(models.Growth).filter(models.Growth.id == growth_id).first()
    if db_growth is None:
        raise HTTPException(status_code=404, detail='Growth record not found')
    db.delete(db_growth)
    db.commit()