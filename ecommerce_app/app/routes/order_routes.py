from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from app.schemas.order_schema import CreateOrder
from app.core.database import order_collection, cart_collection, product_collection
from app.core.crud import MongoCRUD

router = APIRouter()

order_crud = MongoCRUD(order_collection)
product_crud = MongoCRUD(product_collection)

# fetch all order
@router.get("/order")
def get_orders():
    orders = []
    for order in order_collection.find():
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

# fetch order based on the order id 
@router.get("/order/{order_id}")
def get_order(order_id: str):
    order = order_collection.find_one({"order_id": order_id})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["_id"] = str(order["_id"])
    return order

# create an order 
@router.post("/order")
def create_order(data: CreateOrder):

    #  Get cart
    cart = cart_collection.find_one({"user_id": data.user_id})
    if not cart or not cart["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_items = []
    total = 0

    for item in cart["items"]:
        product = product_crud.get_by_product_id(item["product_id"])

        subtotal = product["price"] * item["quantity"]
        total += subtotal

        order_items.append({
            "product_id": product["product_id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": item["quantity"],
            "subtotal": subtotal
        })

    order_data = {
        "order_id": uuid.uuid4().hex[:12].upper(),
        "user_id": data.user_id,
        "items": order_items,
        "total_amount": total,
        "status": "PLACED",
        "created_at": datetime.utcnow()
    }

    order_collection.insert_one(order_data)

    #  Clear cart after order
    cart_collection.delete_one({"user_id": data.user_id})

    return {
        "message": "Order placed successfully",
        "order_id": order_data["order_id"]
    }

# update the order status
@router.put("/order/{order_id}/status")
def update_order_status(order_id: str, status: str):

    result = order_collection.update_one(
        {"order_id": order_id},
        {"$set": {"status": status}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order status updated"}
