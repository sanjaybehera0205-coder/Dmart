from pymongo import MongoClient

MONGO_URL = "mongodb+srv://sanjaybehera0205_db_user:Qwerty123@project.2epebin.mongodb.net/ecommerce_db?retryWrites=true&w=majority&appName=project"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    print("MongoDB server version:", client.server_info()["version"])
    print("✅ MongoDB Atlas connection SUCCESS")
except Exception as e:
    print("❌ MongoDB Atlas connection FAILED")
    print(e)
