from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery as user
import BaseDeDatos.ProjectsQuery as Proj
from pymongo import errors
from datetime import date
from bson.objectid import ObjectId

def CrearTablaSueldos(id_proyecto):
    """
    Función para crear la tabla de sueldos en el proyecto
    Argumentos
    id_proyecto--> ObjectID del proyecto al que se asociará la tabla
    """
    # Los sueldos corresponden a una lista de tuplas (miembro, sueldo) en dólares
    Sueldos = []

    query = {
            "id_proyecto": id_proyecto,
            "Sueldos": Sueldos
            }

    try : 
        db["Sueldos"].insert_one(query)
        print("Doc de requerimientos creado con éxito")
    except Exception as e:
        print(e)

def AgregarSueldos(id_proyecto, email_miembro, sueldo):
    """
    Función para agregar el sueldo de un miembro
    Argumentos
    id_proyecto--> ObjectID del proyecto
    email_miembro--> correo del miembro a asignar su sueldo
    sueldo--> cantidad del sueldo a asignar, en dólares
    """

    # Buscar la tabla de sueldos asignada al proyecto
    proyecto = collection.find_one(ObjectId(id_proyecto))
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return
