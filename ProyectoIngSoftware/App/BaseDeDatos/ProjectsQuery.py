from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery as user
import BaseDeDatos.ReqCompQuery as Req
from bson.objectid import ObjectId

def CrearNuevoProyecto(Nombre, participantes: list, email_user):
    owner = email_user
    if Nombre == "":
        nombre_proyecto = "Proyecto sin nombre"
    else:
        nombre_proyecto = Nombre
    integrantes = []
    for persona in participantes:
        integrantes.append(persona)
    id_proyecto = 111 + user.BuscarProyectos(owner)

    tablaVAC = {"ComunicacionDeDatos" : 0,
        "ProcesamientoDistribuido" : 0,
        "ObjetivosDeRendimiento": 0,
        "ConfiguracionDelEquipamiento" : 0,
        "TasaDeTransacciones" : 0,
        "EntradaDeDatosEnLinea" : 0,
        "InterfaseConElUsuario" : 0,
        "ActualizacionEnLinea" : 0,
        "ProcesamientoComplejo" : 0,
        "ReusabilidadDelCodigo" : 0,
        "FacilidadDeImplementacion" : 0,
        "FacilidadDeOperacion" : 0,
        "InstalacionesMultiples" : 0,
        "FacilidadDeCambios" : 0,
        "TotalFactorAjuste" : 0}
    

    db['Projects'].insert_one({'owner':owner,
                                'id':id_proyecto, 
                                'nombre':nombre_proyecto, 
                                "integrantes": integrantes,
                                "TablaVAC": tablaVAC,
                                })
    doc = db['Projects'].find_one({'owner': email_user, 'id': id_proyecto})
    object_id = doc['_id']
    Req.CrearColeccionDeRequerimientos(ObjectId(object_id))
"""
self.documento = db['Projects'].find_one({'owner': self.user_email, 'id': self.ID_activo})
        if self.documento:
            self.object_id = self.documento['_id']
"""
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
        nombre_proyecto = proyecto['nombre']
        integrantes = proyecto['integrantes']
        id_proyecto = proyecto['id']
        tablaVAC = proyecto['TablaVAC']

        return [nombre_proyecto, integrantes, id_proyecto, tablaVAC]
    else:
        print("No se encontró el proyecto")
        return None
    
def ObtenerNombreProyecto(email_user, id_proyecto):
    """Funcion que retorna el nombre de un proyecto"""
    

def ObtenerNombresProyecto(email_user):
    """
    Funcion que retorna una lista con los nombres de los proyectos del usuario
    """

    proyectos = db['Projects'].find({'owner': email_user})

    # Extraer y devolver los nombres de los proyectos
    nombres_proyectos = [proyecto['nombre'] for proyecto in proyectos]
    return nombres_proyectos
    
def ObtenerIdProyecto(email_user:str, nombre:str):
    proyecto = db['Projects'].find_one({'owner': email_user, 'nombre': nombre})
    if proyecto:
        return proyecto.get('id')
    else:
        print("No se encontró el proyecto.")
    
def AumentarProyectos(email: str) -> None:#Se eliminó la condición de tener menos de 3 proyectos
    '''Aumenta el numero de proyectos del usuario'''
    if user.BuscarUsuario(email):
        usuario = db['Users'].find_one({'email': email}, {'proyectos': 1})
        n_proyectos = usuario['proyectos']
        # Incrementa el valor de "proyectos"
        db['Users'].update_one(
            {'email': email},
            {'$set': {'proyectos': n_proyectos + 1}}
        )
        print(f"Proyectos incrementados a: {n_proyectos + 1}")
    else:
        print("El usuario no existe")


"""def BuscarProyectos(email: str)-> int:
    
    #Función que busca y retorna la cantidad de proyectos del usuario
    
    if (user.BuscarUsuario(email)):
        usuario = db['Users'].find_one({'email': email}, {'proyectos': 1})
        n_proyectos = usuario['proyectos']
        return n_proyectos
    else:
        print("Error: No se encontró el usuario (Buscarproyectos)")"""

def SetearProyectos(email:str)->None:
    """Función que setea los proyectos del usuario en 0"""
    if (user.BuscarUsuario(email)):
        db['Users'].update_one({'email': email},{'$set': {'proyectos': 0}})
    else:
        print("Error: No se encontró el usuario (Setearproyectos)")

#HACER FUNCION PARA DISMINUIR EN 1 LOS PROYECTOS DEL USUARIO (ELIMINAR)

def EliminarProyecto(email_user: str, id_proyecto: int)->bool:
    '''Elimina un proyecto de la base de datos'''
    if (BuscarProyecto(email_user, id_proyecto)):
        db['Projects'].delete_one({'owner':email_user, 'id':id_proyecto})
        print(f'Proyecto con id "{id_proyecto}" eliminado.')
        if user.BuscarUsuario(email_user):
            usuario = db['Users'].find_one({'email': email_user}, {'proyectos': 1})
            n_proyectos = usuario['proyectos']
            # Decrementa el valor de "proyectos"
            db['Users'].update_one(
                {'email': email_user},
                {'$set': {'proyectos': n_proyectos - 1}}
            )
            print(f"Proyectos decrementados a: {n_proyectos -1}")
        else:
            print("El usuario no existe")
        return True
    else:
        print(f'El proyecto que intentas eliminar no existe')
        return False
    
