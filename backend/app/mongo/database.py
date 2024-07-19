from pymongo.mongo_client import MongoClient
# TODO uncomment later
# from config import settings

#uri = f"mongodb+srv://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_hostname}/?appName=Cluster0"
uri_2 = "mongodb+srv://lamakhaled789:mSgyWhRQwrkiNeub@cluster0.kayobza.mongodb.net/?appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri_2)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
mongo_db = client.reviews_db
english_collection = mongo_db["english_reviews"]
ar_collection = mongo_db["arabic_reviews"]

