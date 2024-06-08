from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery_new as user
import BaseDeDatos.ProjectsQuery as Proj
from pymongo import MongoClient, errors

def IngresarInvitacion(owner:str, id_proyecto:int, invitado:str, rol:str, estado:str):
    """Funcion para invitar a un usuario para que\nse una a un proyecto nuevo"""
    
    invitacion = {
        "owner_proyecto":owner,
        "proyecto_id": id_proyecto,
        "correo_invitado": invitado,
        "rol": rol,
        "estado": estado
    }

    try:
        db['Invitaciones'].insert_one(invitacion)
        print("Invitación ingresada correctamente.")
    except errors.ConnectionFailure:
        print("Error: No se pudo conectar a la base de datos.")
    except errors.DuplicateKeyError:
        print("Error: La invitación ya existe.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def ObtenerProyectosAceptados(email:str):
    # Obtener proyectos donde el usuario ha aceptado la invitación
    return list(db['Invitaciones'].find({"correo_invitado": email, "estado": "aceptada"}))