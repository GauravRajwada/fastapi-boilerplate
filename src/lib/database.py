import logging
from pymongo import MongoClient, UpdateMany, UpdateOne
from utils.constants import DATABASE
import os
import logging

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)
logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

PASSWORD = ""
USERNAME = ""
MONGODB_URI = os.getenv("MONGODB_URL", "")
MONGODB_URI = MONGODB_URI.format(USERNAME, PASSWORD)
print(f"MONGODB_URI: {MONGODB_URI}")

class MongoDB:
    """
    MongoDB class to interact with MongoDB database.
    Class handles
    1. Connection with db
    2. Single insertion of data with insert ignore on parameter
    3. Bulk insertion of data with insert ignore on parameter
    4. Update data
    5. Get data with query
    """

    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """
        Establish connection with MongoDB
        """
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DATABASE]
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise

    def disconnect(self):
        """
        Close the MongoDB connection
        """
        if self.client:
            self.client.close()

    def __enter__(self):
        """
        Enter method for context manager
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context manager
        """
        self.disconnect()

    def insert_many(self, collection, data, ignore_on=False):
        """
        Perform bulk insertion of data into the collection 
        """
        if not ignore_on:
            return self.db[collection].insert_many(data)
        try:
            return self.db[collection].insert_many(data, ordered=False).inserted_ids
        except Exception as e:
            # print(f"\n\n e.details: {e.details} \n\n")
            error = e.details.pop('writeErrors', [])
            duplicate_news = [item['op'] for item in error if item['code'] == 11000]
            # logging.info(f"TotalDuplicate news count: {len(duplicate_news)}\n\n")
            logger.info(f"Total Records to be inserted: {len(data)} || Total Duplicate records: {len(duplicate_news)}")

    def insert_one(self, collection, data):
        """
        Perform single insertion of data into the collection
        """
        
        try:
            inserted_id = self.db[collection].insert_one(data).inserted_id
            return {"_id" : str(inserted_id)}
        except Exception as e:
            if e.details.get('code') == 11000:
                logger.info(f"Duplicate record: {data} \n error{e}")
                return {"error": "Duplicate record"}
            raise e
        
    
    def fetch_one(self, collection, query):
        """
        Fetch one data from the collection based on the query
        """
        return self.db[collection].find_one(query)


    def fetch(self, collection, query, limit=None, offset=None):
        """
        Fetch data from the collection based on the query
        """
        try:

            print(f"\n\n base_query: {query}")
            # Create the base query
            base_query = self.db[collection].find(query)
            # Apply limit and offset if provided
            if limit:
                base_query = base_query.limit(limit)
            if offset:
                base_query = base_query.skip(offset)
            
            print(f"\n\n base_query: {base_query}")
            
            return list(base_query)
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def update_one(self, collection, filters, data):
        """
        Update one data in the collection based on the query
        """
        try:
            data = {"$set": data}
            result = self.db[collection].update_one(filters, data)
            if result.modified_count != 0:
                return {"sucess": True}
            return {"sucess": False, "error": "No record updated"}
        except Exception as e:
            if e.details.get('code') == 11000:
                logger.info(f"Duplicate record: {data} \n error{e}")
                return {"sucess": False, "error": e.details.get('errmsg')}
            raise

    def update_many(self, collection, data):
        """
        Update data in the collection based on the query
        """
        update_data = [UpdateMany({"_id": item.pop("_id")}, {"$set": item}) for item in data]
        try:
            result = self.db[collection].bulk_write(update_data)
            return result
        except Exception as e:
            logging.error(f"Error updating data: {e}")
            raise


# # Example usage:
# if __name__ == "__main__":
#     with MongoDB() as db:
#         # 1. Bulk Insertion
#         # data_to_insert = [{"name": "asvfds", "age": 30}, {"name": "afsdvvfds", "age": 25}]
#         data_to_insert = {"name": "asvfdssdfvsf", "age": 30}
#         res = db.insert_one("users", data_to_insert)
#         print("Inserted data:", res)
#         import pdb
#         pdb.set_trace()

#         # 2. Fetch
#         fetched_data = db.fetch("users", {})
#         print("Fetched data:", fetched_data)

#         # 3. Update
#         update_query = {"name": "John"}
#         update_data = {"age": 35}
#         db.update("users", update_query, update_data)

#         # 4. Fetch
#         updated_data = db.fetch("users", {})
#         print("Updated data:", updated_data)