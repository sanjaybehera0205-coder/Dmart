from fastapi import APIRouter, HTTPException,Body
import string
import random
import uuid
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.database import user_collection
from app.core.security import hash_password, verify_password, create_token
from app.core.crud import MongoCRUD

router = APIRouter()
user_crud = MongoCRUD(user_collection)
# Dictionary to store reset tokens temporarily (in production, use DB or Redis)
reset_tokens = {}

@router.post("/register")
def register(user: UserCreate):
    # Check if user already exists
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Generate unique 8-character user_id directly inside the API
    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Prepare user data
    data = {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
    }

    # Save user in database
    user_crud.create(data)

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


@router.post("/forgot-password")
def forgot_password(email: str = Body(..., embed=True)):
    # Check if user exists
    db_user = user_collection.find_one({"email": email})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a reset token (UUID)
    reset_token = str(uuid.uuid4())

    # Save the token with user_id in memory (or DB in production)
    reset_tokens[reset_token] = db_user["user_id"]

    # In real app, send this token via email
    return {
        "message": "Password reset token generated",
        "reset_token": reset_token
    }


@router.post("/reset-password")
def reset_password(reset_token: str = Body(...), new_password: str = Body(...)):
    # Check if token exists
    if reset_token not in reset_tokens:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Get the user_id linked to this token
    user_id = reset_tokens.pop(reset_token)  # Remove token after use

    # Update password in database
    hashed_password = hash_password(new_password)
    result = user_collection.update_one(
        {"user_id": user_id},
        {"$set": {"password": hashed_password}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to reset password")

    return {"message": "Password reset successfully"}
