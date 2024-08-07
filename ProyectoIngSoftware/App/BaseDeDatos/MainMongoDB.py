from pymongo.mongo_client import MongoClient
from pymongo import errors
from bson.objectid import ObjectId
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



def eliminar_todos_los_documentos(coleccion_nombre: str):
    """Elimina todos los documentos de la colección especificada."""
    try:
        resultado = db[coleccion_nombre].delete_many({})
        print(f"Se han eliminado {resultado.deleted_count} documentos de la colección '{coleccion_nombre}'.")
    except errors.ConnectionFailure:
        print("Error: No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def eliminar_coleccion(coleccion_nombre: str):
    """Elimina la colección especificada."""
    try:
        db[coleccion_nombre].drop()
        print(f"La colección '{coleccion_nombre}' ha sido eliminada.")
    except errors.ConnectionFailure:
        print("Error: No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# # Obtén e imprime todas las colecciones
# colecciones = db.list_collection_names()

# print("Colecciones en la base de datos:")
# for coleccion in colecciones:
#     print(coleccion)





# eliminar_todos_los_documentos('Projects')
# eliminar_todos_los_documentos('Invitaciones')
# eliminar_todos_los_documentos('ReqComp')

# db['Users'].update_one({'email': "prueba@gmail.com"},{'$set': {'proyectos': 0}})
# db['Users'].update_one({'email': "prueba2@gmail.com"},{'$set': {'proyectos': 0}})
# doc = db['Projects'].find_one({'owner': "prueba@gmail.com", 'id': 111})['_id']
# print(db['ReqComp'].find_one({"id_proyecto" : ObjectId("667323dfbfa157588b7c113a")}))



"""projects_collection = db['ReqComp']
projects = projects_collection.find()
print("Datos en la colección 'ReqComp':")
for project in projects:
    print(project)"""
