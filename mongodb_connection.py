#This code segment defines the connetion to the MongoDB. 
import asyncio
import pymongo

connection_url = "mongodb://localhost:27017/bookstore"

async def connect_to_mongodb():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(connection_url)
        db = client.get_database()
        collection = db["books"]
        
        # Create indexes
        await collection.create_index("title")  # Create an index on the "title" field
        await collection.create_index("author")  # Create an index on the "author" field
        await collection.create_index("price")  # Create an index on the "price" field

        print("Connected to MongoDB and created indexes!")
        # Add your further database operations here
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB:", str(e))

if __name__ == "__main__":
    # Run the connect_to_mongodb function in an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_to_mongodb())




