from fastapi import FastAPI
import json
from models import Patient

app = FastAPI()

with open('patients.json', 'r') as file:
    # Read Patient JSON data
    patients = json.load(file)

# Get all patients
@app.get("/all_patients")
async def load_patients():
    return {"Patients": patients}

# Create new patient
@app.post("/patient")
async def create_patient(patient: Patient):
    patients.append(patient)
    return {"Patient added": patient}

# Get patient by id
@app.get("/patient/{id}")
async def get_patient(id: int):
    for patient in patients:
        if patient['id'] == id:
            return patient
    return {"message": "Patients printed"}

# Update patient
@app.put("/patient/{id}")
async def get_patient(id: int, patient_update: Patient):
    for patient in patients:
        if patient['id'] == id:
            patient = patient_update
            return patient
    return {"message": "Patients printed"}

# Delete a patient
@app.delete("/patient/{id}")
async def delete_patient(id: int):
    for patient in patients:
        if patient[id] == id:
            patients.remove(patient)
            return {"Patient deleted": id}
    return {"message": "Patient id not found"}
