import BaseDeDatos.MainMongoDB as mDB

db = mDB.client['Application']


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

def ActualizarContrasena(email: str,newPassword: str)->None:
    '''Actualiza la contraseña de un usuario ya registrado.'''
    if (BuscarUsuario(email)):
        db['Users'].update_one({'email': email},{'password': newPassword})
        print(f'Se ha actualizado la contraseña de {email}')
    else:
        print(f'El usuario no existe')

def ValidarUsuario(email: str, password: str)->bool:
    '''Verifica si el usuario existe en la base de datos y que la contraseña ingresada sea correcta.'''
    if (BuscarUsuario(email)):
        if (db['Users'].find_one(email)['password'] == password):
            return True
        else:
            return False
    else:
        return False

def EliminarUsuario(email: str)->None:
    '''Elimina a un usuario de la base de datos'''
    if (BuscarUsuario(email)):
        db['Users'].delete_one({'email':email})
        print(f'Usuario {email} eliminado.')
    else:
        print(f'El usuario que intentas eliminar no existe')