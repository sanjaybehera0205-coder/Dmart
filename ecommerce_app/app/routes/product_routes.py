from fastapi import APIRouter, HTTPException
from app.schemas.product_schema import ProductCreate
from app.core.database import product_collection
from app.core.crud import MongoCRUD
import uuid
from datetime import datetime
router = APIRouter()
product_crud = MongoCRUD(product_collection)


@router.post("/product")
def create_product(product: ProductCreate):
    data = product.dict()

    #  Generate 12-character UUID
    data["product_id"] = uuid.uuid4().hex[:12].upper()

    # ⭐ Default fields
    data["rating"] = 0.0
    data["reviews_count"] = 0
    data["created_at"] = datetime.utcnow()

    # Save to DB
    product_crud.create(data)

    return {
        "message": "Product created successfully",
        "product_id": data["product_id"]
    }


@router.get("/product")
def get_products():
    return product_crud.get_all()


@router.get("/product/{product_id}")
def get_product(product_id: str):
    product = product_crud.get_by_product_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/product/{product_id}")
def update_product(product_id: str, product: ProductCreate):
    updated = product_crud.update(product_id, product.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Update failed")
    return {"message": "Product updated"}


@router.delete("/product/{product_id}")
def delete_product(product_id: str):
    deleted = product_crud.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delete failed")
    return {"message": "Product deleted"}

