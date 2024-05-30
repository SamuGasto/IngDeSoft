from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://ingDeSoft02024:utwbTnVD9VHDGO9n@ingdesoft.u850jdj.mongodb.net/?retryWrites=true&w=majority&appName=IngDeSoft"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Se ha conectado a MongoDB")
except Exception as e:
    print(e)

db = client['Application']
"""
projects_collection = db['Projects']
projects = projects_collection.find()
print("Datos en la colección 'Projects':")
for project in projects:
    print(project)
"""
print(db['Projects'].find_one({'owner' : 'prueba@gmail.com'}))
# db['Projects'].delete_one({'owner':"prueba@gmail.com", 'id':111})
# db['Projects'].delete_one({'owner':"prueba@gmail.com", 'id':112})
# db['Projects'].delete_one({'owner':"prueba@gmail.com", 'id':113})
# db['Users'].update_one({'email': "prueba@gmail.com"},{'$set': {'proyectos': 0}})