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

def AgregarSueldos(id_proyecto, email_miembro, sueldo):
    """
    Función para agregar el sueldo de un miembro
    Argumentos
    id_proyecto--> ObjectID del proyecto
    email_miembro--> correo del miembro a asignar su sueldo
    sueldo--> cantidad del sueldo a asignar, en dólares
    """

    """ # Buscar la tabla de sueldos asignada al proyecto
    sueldo_doc = collection.find_one(ObjectId(id_proyecto))
    if not sueldo_doc:
        print(f"Colección de sueldos con id {id_proyecto} no encontrada")
        return""" #####IGNORAR

    try:
        db["Sueldos"].update_one(
            {'id_proyecto': id_proyecto},
            {'$push': {"Sueldos": (email_miembro, sueldo)}}
        )
    except Exception as e:
        print(e)
