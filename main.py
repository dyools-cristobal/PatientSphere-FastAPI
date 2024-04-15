from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
# api
from apis.patients import router as patients_router
from apis.users import router as users_router
from apis.roles import router as roles_router
from apis.growth import router as growth_router
from apis.clinics import router as clinics_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(patients_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(growth_router)
app.include_router(clinics_router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
