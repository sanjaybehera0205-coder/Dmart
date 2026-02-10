from bson import ObjectId

class MongoCRUD:
    def __init__(self, collection):
        self.collection = collection

    # CREATE
    def create(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)
    
    # READ ALL
    def get_all(self):
        results = []
        for item in self.collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
        return results

    # UPDATE
    def update(self, id: str, data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        return result.modified_count > 0

    def delete(self, user_id: str):
        # Use your custom user_id field
        result = self.collection.delete_one({"user_id": user_id})
        return result.deleted_count


