from fastapi import APIRouter, HTTPException
from app.schemas.product_schema import ProductCreate
from app.core.database import product_collection
from app.core.crud import MongoCRUD

router = APIRouter()
product_crud = MongoCRUD(product_collection)


@router.post("/")
def create_product(product: ProductCreate):
    product_id = product_crud.create(product.dict())
    return {"message": "Product created", "id": product_id}


@router.get("/")
def get_products():
    return product_crud.get_all()


@router.get("/{product_id}")
def get_product(product_id: str):
    product = product_crud.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}")
def update_product(product_id: str, product: ProductCreate):
    updated = product_crud.update(product_id, product.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Update failed")
    return {"message": "Product updated"}


@router.delete("/{product_id}")
def delete_product(product_id: str):
    deleted = product_crud.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delete failed")
    return {"message": "Product deleted"}
