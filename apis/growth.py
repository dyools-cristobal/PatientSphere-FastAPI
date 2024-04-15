from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated 
import models
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

class GrowthBase(BaseModel):
    appointment_id: int
    patient_id: int
    date_taken: str
    height: Decimal
    weight: Decimal
    head_circ: Decimal
    chest_circ: Decimal
    bmi: Decimal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# get all patient growth by id
@router.get("/growth/{patient_id}", status_code=status.HTTP_200_OK)
async def read_user(patient_id: int, db: db_dependency):
    growth = db.query(models.Growth).filter(models.Growth.patient_id == patient_id).all()
    if growth is None:
        raise HTTPException(status_code=404, detail='No growth records found')
    return growth

#create growth
@router.post("/growth/", status_code=status.HTTP_201_CREATED)
async def create_growth(growth:GrowthBase, db: db_dependency):
    db_growth = models.Growth(**growth.dict())
    db.add(db_growth)
    db.commit()

#update growth
@router.put("/growth/{growth_id}", status_code=status.HTTP_200_OK)
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
@router.delete("/growth/{growth_id}",status_code=status.HTTP_200_OK)
async def delete_growth(growth_id: int, db:db_dependency):
    db_growth = db.query(models.Growth).filter(models.Growth.id == growth_id).first()
    if db_growth is None:
        raise HTTPException(status_code=404, detail='Growth record not found')
    db.delete(db_growth)
    db.commit()