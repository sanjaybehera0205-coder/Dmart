from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate
from app.core.database import user_collection
from app.core.crud import MongoCRUD
from app.core.security import hash_password

router = APIRouter()
user_crud = MongoCRUD(user_collection)


# CREATE USER
@router.post("/")
def create_user(user: UserCreate):
    data = user.dict()
    data["password"] = hash_password(data["password"])

    user_id = user_crud.create(data)
    return {"message": "User created", "id": user_id}


# GET ALL USERS
@router.get("/")
def get_users():
    users = user_crud.get_all()
    for u in users:
        u.pop("password", None)
    return users


# GET USER BY ID
@router.get("/{user_id}")
def get_user(user_id: str):
    user = user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.pop("password", None)
    return user


# UPDATE USER
@router.put("/{user_id}")
def update_user(user_id: str, user: UserCreate):
    data = user.dict()
    data["password"] = hash_password(data["password"])

    updated = user_crud.update(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Update failed")

    return {"message": "User updated"}


# DELETE USER
@router.delete("/{user_id}")
def delete_user(user_id: str):
    deleted = user_crud.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delete failed")

    return {"message": "User deleted"}
