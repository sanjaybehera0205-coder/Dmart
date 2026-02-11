from bson import ObjectId

class MongoCRUD:
    def __init__(self, collection):
        self.collection = collection

    # CREATE
    def create(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)
    
    # get by product id 
    def get_by_product_id(self, product_id: str):
        item = self.collection.find_one({"product_id": product_id})
        if item:
            item["_id"] = str(item["_id"])
        return item

    # READ ALL
    def get_all(self):
        results = []
        for item in self.collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
        return results

    # UPDATE
    def update(self, product_id: str, data: dict):
        result = self.collection.update_one(
            {"product_id": product_id},   # ✅ use custom field
            {"$set": data}
        )
        return result.modified_count > 0
    
    def delete(self, product_id: str):
        result = self.collection.delete_one(
            {"product_id": product_id}   # ✅ use product_id
        )
        return result.deleted_count > 0



