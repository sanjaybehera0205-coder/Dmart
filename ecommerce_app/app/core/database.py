from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# ⚠️ NEVER hardcode password in real projects
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://sanjaybehera0205_db_user:Sanju123@dev.yle4vo1.mongodb.net/?appName=dev"
)

# Create MongoDB client
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

# Test connection
try:
    client.admin.command("ping")
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)

# Database
db = client["ecommerce_db"]

# Collections
user_collection = db["users"]
product_collection = db["products"]
cart_collection = db["carts"]
order_collection = db["orders"]
