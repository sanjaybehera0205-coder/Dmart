from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.cart_schema import AddToCart
from app.core.database import cart_collection, product_collection
from app.core.crud import MongoCRUD

router = APIRouter()

cart_crud = MongoCRUD(cart_collection)
product_crud = MongoCRUD(product_collection)

@router.get("/cart/{user_id}")
def get_cart(user_id: str):
    cart = cart_collection.find_one({"user_id": user_id})

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart["_id"] = str(cart["_id"])
    return cart

@router.post("/cart/add")
def add_to_cart(data: AddToCart):

    # 🔍 Check product exists
    product = product_crud.get_by_product_id(data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = cart_collection.find_one({"user_id": data.user_id})

    subtotal = product["price"] * data.quantity

    if cart:
        items = cart["items"]

        # If product already exists in cart
        for item in items:
            if item["product_id"] == data.product_id:
                item["quantity"] += data.quantity
                break
        else:
            items.append({
                "product_id": data.product_id,
                "quantity": data.quantity
            })

        # Recalculate total
        total = 0
        for item in items:
            prod = product_crud.get_by_product_id(item["product_id"])
            total += prod["price"] * item["quantity"]

        cart_collection.update_one(
            {"user_id": data.user_id},
            {
                "$set": {
                    "items": items,
                    "total_amount": total,
                    "updated_at": datetime.utcnow()
                }
            }
        )

    else:
        cart_data = {
            "user_id": data.user_id,
            "items": [
                {
                    "product_id": data.product_id,
                    "quantity": data.quantity
                }
            ],
            "total_amount": subtotal,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        cart_collection.insert_one(cart_data)

    return {"message": "Product added to cart"}

@router.delete("/cart/{user_id}/{product_id}")
def remove_from_cart(user_id: str, product_id: str):

    cart = cart_collection.find_one({"user_id": user_id})

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = [item for item in cart["items"] if item["product_id"] != product_id]

    if len(items) == len(cart["items"]):
        raise HTTPException(status_code=404, detail="Product not in cart")

    total = 0
    for item in items:
        prod = product_crud.get_by_product_id(item["product_id"])
        total += prod["price"] * item["quantity"]

    cart_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "items": items,
                "total_amount": total,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {"message": "Product removed from cart"}
