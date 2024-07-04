from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery as user
import BaseDeDatos.ProjectsQuery as Proj
from pymongo import errors
from datetime import date
from bson.objectid import ObjectId

collection = db["ReqComp"]

def CrearColeccionDeRequerimientos(id_proyecto):
    """
    Función que crea un documento para los requerimientos de un proyecto nuevo.
    """
    query = {
            "id_proyecto": id_proyecto, #id de mongoDB. Acá se asocia el proyecto con los requerimientos
            "Requerimientos": [],
            "Puntos_de_funcion": {"Atributos":[]}
            }   

    try : 
        db["ReqComp"].insert_one(query)
        print("Doc de requerimientos creado con éxito")
    except Exception as e:
        print(e)

def AgregarRequerimientos(id_proyecto:int, reques:list):
    """
    Función para agregar requerimientos a un doc de proyecto existente.
    
    reques --> [Requerimiento : str]
    id_proyecto --> ObjectId de MongoDB
    """

    # Buscar el proyecto en la base de datos
    proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return

    # Obtener los requerimientos actuales del proyecto
    requerimientos = proyecto.get("Requerimientos", [])

    # Determinar el último ID utilizado
    if requerimientos:
        ultimo_id = max(int(req["ID"].split('-')[1]) for req in requerimientos)
    else:
        ultimo_id = 0

    # Lista que contiene cada requerimiento con sus datos.
    lista_de_requerimientos = []
    
    # Asignar IDs globales a los nuevos requerimientos
    for req in reques:
        ultimo_id += 1
        nuevo_id = f"REQ-{ultimo_id:03d}"
        requerimiento = {
            "ID": nuevo_id,
            "Asignado": None, # email del miembro de equipo asignado
            "Descripción": req,
            "FechaAsignación": f"{date.today()}",
            "Estimado": False,
            "Componentes": []  # Al ingresar requerimientos, vienen sin componentes
        }
        lista_de_requerimientos.append(requerimiento)

    try: 
        db["ReqComp"].update_one(
            {'id_proyecto': id_proyecto},
            {'$push': {'Requerimientos': {'$each': lista_de_requerimientos}}}
        )
        print("Requerimientos agregados con éxito")
    except Exception as e:
        print(e)


    

def AgregarComponentes(id_proyecto, id_requerimiento, componentes):
    """
    Función para agregar componentes a un requerimiento específico de un proyecto.
    
    id_proyecto --> ObjectId del proyecto de MongoDB
    id_requerimiento --> ID del requerimiento dentro del proyecto
    componentes --> lista de componentes a agregar, cada componente es un diccionario
    """
    
    # Definir la estructura de un componente
    Componente = { 
        "ID": int,
        "Descripcion": str,
        "Tipo": str, # in (0,1,2,3,4)
        "Atributos": int,
        "PF": int, # automático desde atributos
        "PF_own": (bool, int),
        "Razon": str
    }

    # Buscar el proyecto y requerimiento específico
    proyecto = collection.find_one(ObjectId(id_proyecto))
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return

    # Buscar el requerimiento específico
    requerimientos = proyecto.get("Requerimientos", [])
    requerimiento = None
    for req in requerimientos:
        if req["ID"] == id_requerimiento:
            requerimiento = req
            break

    if not requerimiento:
        print(f"Requerimiento con id {id_requerimiento} no encontrado en el proyecto")
        return

    # Lista para agregar nuevos componentes
    lista_de_componentes = requerimiento.get("Componentes", [])

    # Añadir los componentes a la lista
    j = len(lista_de_componentes)
    for comp in componentes:
        nuevo_componente = Componente.copy()
        nuevo_componente["ID"] = j
        nuevo_componente["Descripcion"] = comp["Descripcion"]
        nuevo_componente["Tipo"] = comp["Tipo"]
        nuevo_componente["Atributos"] = comp["Atributos"]
        nuevo_componente["PF"] = comp["Atributos"]  # Suponiendo que PF se calcula automáticamente desde atributos
        nuevo_componente["PF_own"] = comp["PF_own"]
        nuevo_componente["Razon"] = comp["Razon"]
        lista_de_componentes.append(nuevo_componente)
        j += 1

    # Actualizar el requerimiento con los nuevos componentes
    collection.update_one(
        {"id_proyecto": id_proyecto, "Requerimientos.ID": id_requerimiento},
        {"$set": {"Requerimientos.$.Componentes": lista_de_componentes}}
    )

    print("Componentes agregados con éxito")
    print(lista_de_componentes)

def ObtenerRequerimientos(id_proyecto) ->list :
    """
    Función para obtener los requerimientos de un proyecto.
    
    id_proyecto --> ObjectId del proyecto de MongoDB

    return ->> lista de tuplas ("ID", "Texto", "Asignado", "Estimado")
    """
    
    # Buscar el proyecto en la base de datos
    proyecto = collection.find_one({"id_proyecto" : ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return []

    # Obtener los requerimientos del proyecto
    requerimientos = proyecto.get("Requerimientos", [])

    # Crear una lista de tuplas con el ID del requerimiento y la descripción
    lista_de_requerimientos = [(req["ID"], req["Descripción"], req["Asignado"], req["Estimado"]) for req in requerimientos]

    return lista_de_requerimientos

def AsignarMiembro(id_proyecto, email_miembro, req_id):
    """
    Funcion para asignar un miembro (email) a un requerimiento específico.
    Argumentos:
    id_proyecto --> ObjectId del proyecto de MongoDB
    email_miembro --> email de quién se va a asignar
    req_id --> ID del requerimiento dentro del proyecto
    """
    # Buscar el proyecto en la base de datos
    proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return

    # Buscar el requerimiento específico
    requerimientos = proyecto.get("Requerimientos", [])
    requerimiento = None
    for req in requerimientos:
        if req["ID"] == req_id:
            requerimiento = req
            break

    if not requerimiento:
        print(f"Requerimiento con id {req_id} no encontrado en el proyecto")
        return

    # Asignar el email del miembro al requerimiento
    requerimiento["Asignado"] = email_miembro

    # Actualizar el documento en la base de datos
    collection.update_one(
        {"id_proyecto": id_proyecto, "Requerimientos.ID": req_id},
        {"$set": {"Requerimientos.$.Asignado": email_miembro}}
    )

    print(f"Miembro {email_miembro} asignado al requerimiento {req_id} con éxito")


"""
#CÓDIGO QUE PODRÍA SERVIR(para cuando se agreguen los componentes)

puntos_de_funcion_totales = 0
    for req in lista_de_requerimientos:#iteramos sobre un diccionario
        compo = req["Componentes"]#es una lista
        for dicc in compo:
            pf = dicc["PF"]
            if pf == None:
                break
            else:
                puntos_de_funcion_totales += pf


"""