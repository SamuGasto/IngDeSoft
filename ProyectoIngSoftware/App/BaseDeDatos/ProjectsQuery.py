from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery_new as user

def CrearNuevoProyecto(Nombre, participantes, email_user):
    owner = email_user
    if Nombre == "":
        nombre_proyecto = "Proyecto sin nombre"
    else:
        nombre_proyecto = Nombre
    integrantes = []
    for persona in participantes:
        integrantes.append(persona)
    id_proyecto = 110 + user.BuscarProyectos(owner)

    db['Projects'].insert_one({'owner':owner,
                                'id':id_proyecto, 
                                'nombre':nombre_proyecto, 
                                "integrantes": integrantes, 
                                })

def BuscarProyecto(email_user, id_proyecto):
    '''Busca el proyecto en la base de datos'''
    if (db['Projects'].find_one({'owner':email_user, 'id': id_proyecto}) != None):
        return True
    return False

def ObtenerDatosProyecto(email_user, id_proyecto):
    """
    Función que retorna los datos de un proyecto.

    Retorna [nombre_proyecto, lista_integrantes, id_proyecto]
    """
    proyecto = db['Projects'].find_one({'owner': email_user, 'id': id_proyecto})
    if proyecto:
        nombre_proyecto = proyecto.get('nombre')
        integrantes = proyecto.get('integrantes')
        id_proyecto = proyecto.get('id')

        return [nombre_proyecto, integrantes, id_proyecto]
    else:
        print("No se encontró el proyecto")
        return None
    
def ObtenerIdProyecto(email_user:str, nombre:str):
    proyecto = db['Projects'].find_one({'owner': email_user, 'nombre': nombre})
    if proyecto:
        return proyecto.get('id')
    else:
        print("No se encontró el proyecto.")
    
def AumentarProyectos(email: str)->None:
    '''Aumenta el numero de proyectos del usuario'''
    if (user.BuscarUsuario(email)):
        usuario = db['Users'].find_one({'email': email}, {'proyectos': 1})
        n_proyectos = usuario['proyectos']
        if  n_proyectos <= 3:
            # Incrementa el valor de "proyectos"
            db['Users'].update_one(
                {'email': email},
                {'$set': {'proyectos': n_proyectos + 1}}
            )
            print(f"Proyectos incrementados a: {n_proyectos + 1}")
            n_proyectos = usuario['proyectos']
        else:
            print("El usuario ya tiene 3 proyectos.")
    else:
        print("El usuario no existe (Aumentarproyectos)")

def BuscarProyectos(email: str)-> None:
    """
    Función que busca y retorna la cantidad de proyectos del usuario
    """
    if (user.BuscarUsuario(email)):
        usuario = db['Users'].find_one({'email': email}, {'proyectos': 1})
        n_proyectos = usuario['proyectos']
        return n_proyectos
    else:
        print("Error: No se encontró el usuario (Buscarproyectos)")

def SetearProyectos(email:str)->None:
    """Función que setea los proyectos del usuario en 0"""
    if (user.BuscarUsuario(email)):
        db['Users'].update_one({'email': email},{'$set': {'proyectos': 0}})
    else:
        print("Error: No se encontró el usuario (Setearproyectos)")

def EliminarProyecto(email_user: str, id_proyecto: int)->bool:
    '''Elimina un proyecto de la base de datos'''
    if (BuscarProyecto(email_user, id_proyecto)):
        db['Projects'].delete_one({'owner':email_user, 'id':id_proyecto})
        print(f'Proyecto con id "{id_proyecto}" eliminado.')
        return True
    else:
        print(f'El proyecto que intentas eliminar no existe')
        return False