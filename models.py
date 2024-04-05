from decimal import Decimal
from fastapi import FastAPI
from pydantic import BaseModel

from typing import List, Optional

class Patient(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    photo_link: Optional[str]
    
    class PhysicalDetails(BaseModel):
        gender: Optional[str]
        age_of_gestation: Optional[Decimal]
        birth_weight: Optional[Decimal]
        birth_length: Optional[Decimal]
        head_circumference: Optional[Decimal]
        chest_circumference: Optional[Decimal]
        abdomen_circumference: Optional[Decimal]
        newborn_screening: Optional[str]
        blood_type: Optional[str]
        known_allergies: List[str]
        perinatal_history: Optional[str]
        date_of_birth: Optional[str]
        time_of_birth: Optional[str]

    class ParentDetails(BaseModel):
        
        class MotherDetails(BaseModel):
            first_name: Optional[str]
            last_name: Optional[str]
            age: Optional[Decimal]
            occupation: Optional[str]
            contact_number: Optional[str]
            email_address: Optional[str]

        class FatherDetails(BaseModel):
            first_name: Optional[str]
            last_name: Optional[str]
            age: Optional[Decimal]
            occupation: Optional[str]
            contact_number: Optional[str]
            email_address: Optional[str]

        class HomeDetails(BaseModel):
            address: Optional[str]
            home_address: Optional[str]

        mother_details: MotherDetails
        father_details: FatherDetails
        home_details: HomeDetails    

    physical_details: PhysicalDetails
    parent_details: ParentDetails