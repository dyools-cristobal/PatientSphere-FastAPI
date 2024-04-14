from http.client import HTTPException
from fastapi import FastAPI
import json
from models import Role, User

app = FastAPI()
with open('users.json', 'r') as file:
    # Read Patient JSON data
    users_db = json.load(file)

@app.post("/login")
def login(user: User):
    if user.username in users_db and users_db[user.username]["password"] == user.password:
        return {"username": user.username, "role": users_db[user.username]["role"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
