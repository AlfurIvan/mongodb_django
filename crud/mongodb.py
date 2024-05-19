from pymongo import MongoClient
from mongo_crud.settings import MONGO_CONN_STR


class MongoDBClient:
    def __init__(self, database="Labs"):
        uri = MONGO_CONN_STR
        self.client = MongoClient(uri)
        self.db = self.client[database]

    def list_databases(self):
        return self.client.list_database_names()

    def list_collections(self):
        return self.db.list_collection_names()

    def list_documents(self, collection_name, filter=None):
        collection = self.db[collection_name]
        return list(collection.find(filter or {}))

    def add_document(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def add_documents(self, collection_name, documents):
        collection = self.db[collection_name]
        result = collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    def update_document(self, collection_name, filter, update):
        collection = self.db[collection_name]
        result = collection.update_one(filter, {'$set': update})
        return result.matched_count, result.modified_count

    def update_documents(self, collection_name, filter, update):
        collection = self.db[collection_name]
        result = collection.update_many(filter, {'$set': update})
        return result.matched_count, result.modified_count

    def delete_document(self, collection_name, filter):
        collection = self.db[collection_name]
        result = collection.delete_one(filter)
        return result.deleted_count

    def delete_documents(self, collection_name, filter):
        collection = self.db[collection_name]
        result = collection.delete_many(filter)
        return result.deleted_count
