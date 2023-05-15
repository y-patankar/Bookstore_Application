import asyncio
import pymongo

connection_url = "mongodb://localhost:27017/bookstore"

async def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(connection_url)
        db = client.get_database()
        collection = db["books"]
        
        # Create indexes
        await collection.create_index("title")
        await collection.create_index("author")
        await collection.create_index("price")

        print("Connected to MongoDB and created indexes!")
        # Add your further database operations here
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB:", str(e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_to_mongodb())



