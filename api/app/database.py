from pymongo import mongo_client
import pymongo
import dependencies

client = mongo_client.MongoClient(
    dependencies.DATABASE_URL, serverSelectionTimeoutMS=5000
)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client[dependencies.MONGO_INITDB_DATABASE]
User = db.users
User.create_index([("email", pymongo.ASCENDING)], unique=True)
