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
            }   

    try : 
        db["ReqComp"].insert_one(query)
        print("Doc de requerimientos creado con éxito")
    except Exception as e:
        print(e)

def AgregarRequerimientos(id_proyecto:int, reques:list):
    """
    Función para agregar requerimientos a\nun doc de proyecto existente.
    
    reques --> [Requerimiento : str]
    id_proyecto --> ObjectId de MongoDB
    """

    lista_de_requerimientos = [] #Lista que contiene cada requerimiento con sus datos.
    id = 0

    reques_W_id = [] #Creamos una lista nueva de requerimientos con un id
    for req in reques:
        reques_W_id.append((id,req))
        id +=1
    """
    reques_W_id --> [ (0,texto_req1), (1,texto_req1), ... , (N-1,texto_reqN) ]
    """

    # Aquí recorremos todos los requerimientos recibidos
    # para agregarlos a la colección.
    for req in reques_W_id:
        id_req = req[0]  # obtenemos el id de la nueva lista
        descripcion = req[1]  # Guardamos el texto del requerimiento

        requerimiento = {
            "ID": id_req,
            "Asignado": None,
            "Descripción": descripcion,
            "FechaAsignación": f"{date.today()}",
            "Estimado": False,
            "Componentes": []  # Al ingresar requerimientos, vienen sin componentes
        }

        lista_de_requerimientos.append(requerimiento)

    try : 
        db["ReqComp"].update_one({'id_proyecto': id_proyecto},
                                 {'$push': {'Requerimientos': {'$each': lista_de_requerimientos}}})
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
        "Tipo": int, # in (0,1,2,3,4)
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

    return ->> lista de tuplas (id, "req")
    """
    
    # Buscar el proyecto en la base de datos
    proyecto = collection.find_one({"id_proyecto" : ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return []

    # Obtener los requerimientos del proyecto
    requerimientos = proyecto.get("Requerimientos", [])

    # Crear una lista de tuplas con el ID del requerimiento y la descripción
    lista_de_requerimientos = [(req["ID"], req["Descripción"]) for req in requerimientos]

    return lista_de_requerimientos

def AsignarMiembro(email, email_miembro, id_proyecto, id_req):
    return


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