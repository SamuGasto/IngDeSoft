from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://ingDeSoft02024:utwbTnVD9VHDGO9n@ingdesoft.u850jdj.mongodb.net/?retryWrites=true&w=majority&appName=IngDeSoft"
# Create a new client and connect to the server
client = MongoClient(uri,
                     serverSelectionTimeoutMS = 50000,
                     socketTimeoutMS = 50000,
                     connectTimeoutMS = 50000,
                     maxPoolSize = 50,
                     maxIdleTimeMS=30000)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Se ha conectado a MongoDB")
except Exception as e:
    print(e)

db = client['Application']