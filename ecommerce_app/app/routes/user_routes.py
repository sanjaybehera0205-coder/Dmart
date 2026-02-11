from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate
from app.core.database import user_collection
from app.core.crud import MongoCRUD
from app.core.security import hash_password
import uuid

router = APIRouter()
user_crud = MongoCRUD(user_collection)

# CrEATE USER
@router.post("/createuser")
def create_user(user: UserCreate):
    data = user.dict()
    #  Hash password
    data["password"] = hash_password(data["password"])
    #  Generate 8-character unique user_id
    data["user_id"] = uuid.uuid4().hex[:8].upper()
    # Save to DB
    user_crud.create(data)
    return {
        "message": "User created successfully",
        "user_id": data["user_id"]
    }


# GET ALL USERS
@router.get("/fetchuser")
def get_users():
    users = user_crud.get_all()
    for u in users:
        u.pop("password", None)
    return users



@router.put("/updateuser/{user_id}")
def update_user(user_id: str, user: UserCreate):
    data = user.dict()
    data["password"] = hash_password(data["password"])

    # Update using user_id instead of _id
    result = user_collection.update_one({"user_id": user_id}, {"$set": data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Update failed")

    return {"message": "User updated successfully"}



@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    # Delete by the custom user_id field
    deleted = user_crud.collection.delete_one({"user_id": user_id})
    
    if deleted.deleted_count > 0:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
