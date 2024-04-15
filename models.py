from decimal import Decimal
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, Float, Date, Time
from database import Base
from typing import List, Optional

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer)
    clinic_id = Column(Integer)
    username = Column(String(50), unique=True)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(50))

class Clinic(Base):
    __tablename__ = 'clinics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    address = Column(String(50))
    phone_number = Column(String(50))

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    dr_id = Column(Integer)
    first_name = Column(String(50))
    middle_name = Column(String(50))
    last_name = Column(String(50))
    photo_link = Column(String(150))
    gender = Column(Integer)
    age_of_gestation = Column(Float)
    birth_weight = Column(Float)
    birth_length = Column(Float)
    head_circumference = Column(Float)
    chest_circumference = Column(Float)
    abdomen_circumference = Column(Float)
    newborn_screening = Column(String(250))
    blood_type = Column(String(50))
    known_allergies = Column(String(250))
    perinatal_history = Column(String(250))
    date_of_birth = Column(String(12))
    time_of_birth = Column(String(12))
    mother_first_name = Column(String(50))
    mother_last_name = Column(String(50))
    mother_age = Column(Integer)
    mother_occupation = Column(String(50))
    mother_contact_number = Column(String(50))
    mother_email_address = Column(String(50))
    father_first_name = Column(String(50))
    father_last_name = Column(String(50))
    father_age = Column(Integer)
    father_occupation = Column(String(50))
    father_contact_number = Column(String(50))
    father_email_address = Column(String(50))
    home_address = Column(String(150))
    home_phone_number = Column(String(50))

class Growth(Base):
    __tablename__ = 'growth'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer)
    date_taken = Column(Date)
    height = Column(Float)
    weight = Column(Float)