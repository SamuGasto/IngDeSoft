from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery as user
import BaseDeDatos.ProjectsQuery as Proj
from pymongo import errors
from datetime import date
from bson.objectid import ObjectId

collection = db["Sueldos"]

def CrearTablaSueldos(id_proyecto):
    """
    Función para crear la tabla de sueldos en el proyecto
    Argumentos
    id_proyecto--> ObjectID del proyecto al que se asociará la tabla
    """
    # Los sueldos corresponden a una lista de tuplas (miembro, sueldo) en dólares

    query = {
            "id_proyecto": id_proyecto,
            "Sueldos": []
            }

    try : 
        db["Sueldos"].insert_one(query)
        print("Tabla de sueldos creada con éxito")
    except Exception as e:
        print(e)
    

def AgregarSueldo(id_proyecto, email_miembro, sueldo):
    """
    Función para agregar el sueldo de un miembro
    Argumentos
    id_proyecto--> ObjectID del proyecto
    email_miembro--> correo del miembro a asignar su sueldo
    sueldo--> cantidad del sueldo a asignar
    """

    try:
        db["Sueldos"].update_one(
            {'id_proyecto': id_proyecto},
            {'$push': {"Sueldos": (email_miembro, int(sueldo))}}
        )
        print("Sueldo agregado exitosamente")
    except Exception as e:
        print(e)

def ObtenerSueldos(id_proyecto):
    """
    Función para retornar la lista con los sueldos del equipo de proyecto\n
    Con "id_proyecto" se busca la tabla de sueldos asociada.
    """
    # Buscamos la tabla de sueldos asociada al proyecto
    sueldos_proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not sueldos_proyecto:
        print("No se encontró la tabla de sueldos o el proyecto no tiene una tabla asignada")
        return
    
    try:
        salary = sueldos_proyecto.get("Sueldos", [])
        return salary
    
    except Exception as e:
        print(e)