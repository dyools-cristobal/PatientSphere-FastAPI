from datetime import date, time
from decimal import Decimal
from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Optional 
from sqlalchemy import Date, Time
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from apis.growth import router as growth_router

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

#create clinic
@router.post("/clinics/", status_code=status.HTTP_201_CREATED)
async def create_clinic(clinic:ClinicBase, db: db_dependency):
    db_clinic = models.Clinic(**clinic.dict())
    db.add(db_clinic)
    db.commit()

#update clinic
@router.put("/clinics/{clinic_id}", status_code=status.HTTP_200_OK)
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
@router.delete("/clinics/{clinic_id}",status_code=status.HTTP_200_OK)
async def delete_clinic(clinic_id: int, db:db_dependency):
    db_clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if db_clinic is None:
        raise HTTPException(status_code=404, detail='Clinic not found')
    db.delete(db_clinic)
    db.commit()