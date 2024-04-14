from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import json
from models import Patient, User, Role, UserInDB, Token, TokenData

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = "100000"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

with open('patients.json', 'r') as file:
    patients = json.load(file)

with open('users.json', 'r') as file:
    users_db = json.load(file)

#Verify password
def verify_password(basic_pass, hashed_pass):
    return pwd_context.verify(basic_pass, hashed_pass)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in users_db:
        user_data = users_db[username]
        return UserInDB(**user_data)

def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + expires_delta(minutes = 30)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exeption
        
        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exeption
    
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credential_exeption
    
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if get_current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]



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


pwd = get_password_hash("password1")
print(pwd)