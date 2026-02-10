from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.database import user_collection
from app.core.security import hash_password, verify_password, create_token
from app.core.crud import MongoCRUD

router = APIRouter()
user_crud = MongoCRUD(user_collection)

@router.post("/register")
def register(user: UserCreate):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
    }

    user_id = user_crud.create(data)

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "name": user.name
    }


@router.post("/login")
def login(user: UserLogin):
    db_user = user_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
