from BaseDeDatos.MainMongoDB import db
import bcrypt


def BuscarUsuario(email: str)->bool:
    '''Busca al usuario en la base de datos'''
    if (db['Users'].find_one({'email':email}) != None):
        return True
    return False

def BuscarUsername(username: str)->bool:
    """Busca el nombre de usuario en la base de datos"""
    if (db['Users'].find_one({'username':username}) != None):
        return True
    return False

def AnadirUsuario(email: str, username: str, password: str, rol: str)->None:
    '''Añade a un usuario a la base de datos, si ya existe, entonces no hace nada.'''
    if (BuscarUsuario(email)):
        print(f'El usuario {email} ya existe')
        return
    
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    pwdEncrypt = bcrypt.hashpw(pwd,salt)
    second_rol = ""#variable para manejar los roles de cada proyecto
    proyectos = 0

    db['Users'].insert_one({'email':email, 'username': username, 'password': pwdEncrypt.decode('utf-8'),
                            'rol': rol, "second_rol": second_rol, "proyectos": proyectos})
    
def AumentarProyectos(email: str)->None:
    '''Aumenta el numero de proyectos del usuario'''
    if (BuscarUsuario(email)):
        usuario = db['Users'].find_one({'email': email}, {'proyectos': 1})
        n_proyectos = usuario['proyectos']
        if  n_proyectos < 3:
            # Incrementa el valor de "proyectos"
            db['Users'].update_one(
                {'email': email},
                {'$set': {'proyectos': n_proyectos + 1}}
            )
            print(f"Proyectos incrementados a: {n_proyectos + 1}")
            n_proyectos = usuario['proyectos']
            return n_proyectos
        else:
            print("El usuario ya tiene 3 o más proyectos.")
    else:
        print("El usuario no existe")
def BuscarProyectos(email: str)-> None:
    if (BuscarUsuario(email)):
        usuario = db['Users'].find_one({'email': email}, {'proyectos': 1})
        n_proyectos = usuario['proyectos']
        return n_proyectos
    else:
        print("Error")

def SetearProyectos(email:str)->None:
    if (BuscarUsuario(email)):
        db['Users'].update_one({'email': email},{'$set': {'proyectos': 0}})
    else:
        print("Error")

def ActualizarContrasena(email: str,newPassword: str)->None:
    '''Actualiza la contraseña de un usuario ya registrado.'''
    if (BuscarUsuario(email)):
        
        pwd = newPassword.encode('utf-8')
        salt = bcrypt.gensalt()
        pwdEncrypt = bcrypt.hashpw(pwd,salt)

        db['Users'].update_one({'email': email},{'password': pwdEncrypt.decode('utf-8')})
        print(f'Se ha actualizado la contraseña de {email}')
    else:
        print(f'El usuario no existe')

def ValidarUsuario(email: str, password: str)->bool:
    '''Verifica si el usuario existe en la base de datos y que la contraseña ingresada sea correcta.'''
    if (BuscarUsuario(email)):
        if (bcrypt.checkpw(password.encode('utf-8'), db['Users'].find_one({'email' : email})['password'].encode('utf-8'))):
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

