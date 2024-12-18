import os
from pymongo import MongoClient

class NOSQLDB:
    def __init__(self, db_name,connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.get_database(db_name)
        self.db_name = db_name

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def insert(self,collection,data):
        result = self.client.get_database(self.db_name).get_collection(collection).insert_one(data)
        data["_id"] = str(result.inserted_id)
        # Return Created Object with Id
        return data        

    def find(self,collection,query):
        return self.client.get_database(self.db_name).get_collection(collection).find(query)

    def find_one(self,collection,query):
        return self.client.get_database(self.db_name).get_collection(collection).find_one(query)
    
    def update(self,collection,query,new_values):
        self.client.get_database(self.db_name).get_collection(collection).update_one(query,new_values)

    def delete(self,collection,query):
        self.client.get_database(self.db_name).get_collection(collection).delete_one(query)

from dotenv import load_dotenv

load_dotenv()
connection_string = os.environ.get("MONGODB_CONNECTION_STRING")

print("Connection String Initialized")

db = NOSQLDB(
    db_name="xcloud",
    connection_string=connection_string
)

def get_db():
    return db