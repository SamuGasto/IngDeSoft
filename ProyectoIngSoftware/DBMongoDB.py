from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://ingDeSoft02024:utwbTnVD9VHDGO9n@ingdesoft.u850jdj.mongodb.net/?retryWrites=true&w=majority&appName=IngDeSoft"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Application']


def BuscarUsuario(email: str)->bool:
    '''Busca al usuario en la base de datos'''
    if (db['Users'].find_one({'email':email}) != None):
        return True
    return False

def AnadirUsuario(email: str,password: str)->None:
    '''Añade a un usuario a la base de datos, si ya existe, entonces no hace nada.'''
    if (BuscarUsuario(email)):
        print(f'El usuario {email} ya existe')
        return
    db['Users'].insert_one({'email':email, 'password': password})

def EliminarUsuario(email: str)->None:
    db['Users'].delete_one({'email':email})
    print(f'Usuario {email} eliminado.')

def ActualizarContrasena(email: str,newPassword: str)->None:
    db['Users'].update_one({'email': email},{'password': newPassword})
    print(f'Se ha actualizado la contraseña de {email}')