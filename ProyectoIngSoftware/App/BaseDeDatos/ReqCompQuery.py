import string
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
        print(f"Proyecto con id {id_proyecto} no encontrado. agregarrequerimiento")
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
    componentes --> componente a agregar, que es un diccionario
    """
    
    # Definir la estructura de un componente
    Componente = { 
        "IDReq": int,
        "ID": int,
        "Descripcion": str,
        "Tipo": str, 
        "Atributos": int,
        "Complejidad": int,
        "PF": int, # automático desde atributos
        "PF_own": (bool, int),
        "Razon": str
    }

    # Buscar el proyecto y requerimiento específico
    proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado. agergarcomponente")
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

    # Añadir el componente a la lista
    nuevo_componente = Componente.copy()
    nuevo_componente["IDReq"] = componentes[0]
    nuevo_componente["ID"] = componentes[1]
    nuevo_componente["Descripcion"] = componentes[2]
    nuevo_componente["Tipo"] = componentes[3]
    nuevo_componente["Atributos"] = componentes[4]
    nuevo_componente["Complejidad"] = componentes[5]
    nuevo_componente["PF"] = componentes[6]  # Suponiendo que PF se calcula automáticamente desde atributos
    nuevo_componente["PF_own"] = ""
    nuevo_componente["Razon"] = ""


    # Actualizar el requerimiento con los nuevos componentes
    collection.update_one(
        {"id_proyecto": id_proyecto, "Requerimientos.ID": id_requerimiento},
        {"$push": {"Requerimientos.$.Componentes": nuevo_componente}}
    )

    print("Componente agregado con éxito")
    print(nuevo_componente)

def EliminarComponente(id_proyecto, id_requerimiento, componente):
    """
    Función para eliminar un componente presente en un requerimiento.
    id_proyecto --> El ID del proyecto.
    id_requerimiento --> El ID del requerimiento donde esta vinculado el componente.
    componente --> El componente a eliminar.
    """
    
    # Buscar el proyecto y requerimiento específico
    proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado. eliminarcomponente")
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

    collection.update_one({"Requerimientos.Componentes.ID": componente[1]},
                          {"$pull" : {"Requerimientos.$.Componentes" : {"ID" : componente[1]}}})

def ModificarPuntosDeFuncion(id_proyecto, id_req, id_comp, nuevoPuntoDeFuncion, razon: string):
    """
    Función que modifica el punto de función asignado normalmente
    """
    proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado")
        return

    # Buscar el requerimiento específico
    requerimientos = proyecto.get("Requerimientos", [])
    requerimiento = None
    for req in requerimientos:
        if req["ID"] == id_req:
            requerimiento = req
            break

    if not requerimiento:
        print(f"Requerimiento con id {id_req} no encontrado en el proyecto")
        return
    
    collection.update_one({"Requerimientos.Componentes.ID": id_comp},
                          {"$set" : {"Requerimientos.$.Componentes.$[id].PF_own" : nuevoPuntoDeFuncion, "Requerimientos.$.Componentes.$[id].Razon" : razon}}, 
                          array_filters=[{"id.ID" : id_comp}])

def ObtenerRequerimientos(id_proyecto) ->list :
    """
    Función para obtener los requerimientos de un proyecto.
    
    id_proyecto --> ObjectId del proyecto de MongoDB

    return ->> lista de tuplas ("ID", "Texto", "Asignado", "Estimado")
    """
    
    # Buscar el proyecto en la base de datos
    proyecto = collection.find_one({"id_proyecto" : ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado. obtenerrequerimiento")
        return [],[]

    # Obtener los requerimientos del proyecto
    requerimientos = proyecto.get("Requerimientos", [])
    

    # Crear una lista de tuplas con el ID del requerimiento y la descripción
    lista_de_requerimientos = []
    lista_componentes = []

    for req in requerimientos:
        lista_de_requerimientos.append([req["ID"], req["Descripción"], req["Asignado"], req["Estimado"]])
        componentes = req.get("Componentes", [])
        for com in componentes:
            lista_componentes.append([com["IDReq"],com["ID"], com["Descripcion"], com["Tipo"], com["Atributos"], com["Complejidad"], com["PF"], com["PF_own"], com["Razon"]])


    return lista_de_requerimientos, lista_componentes

def AsignarMiembro(id_proyecto, email_miembro, req_text):
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
        print(f"Proyecto con id {id_proyecto} no encontrado. asignarmiembto")
        return

    # Buscar el requerimiento específico
    requerimientos = proyecto.get("Requerimientos", [])
    requerimiento = None
    for req in requerimientos:
        if req["Descripción"] == req_text:
            requerimiento = req
            break

    if not requerimiento:
        print(f"Requerimiento '{req_text}' no encontrado en el proyecto")
        return

    # Asignar el email del miembro al requerimiento
    requerimiento["Asignado"] = email_miembro

    # Actualizar el documento en la base de datos
    collection.update_one(
        {"id_proyecto": id_proyecto, "Requerimientos.Descripción": req_text},
        {"$set": {"Requerimientos.$.Asignado": email_miembro}}
    )

    print(f"Miembro {email_miembro} asignado al requerimiento con éxito")

def CalcularpfTotal(id_proyecto):
    """
    Función para calcular la suma total de PF de todos los componentes de cada requerimiento en un proyecto.
    
    id_proyecto --> ObjectId del proyecto de MongoDB
    """

    # Buscar el proyecto en la base de datos
    proyecto = collection.find_one({"id_proyecto": ObjectId(id_proyecto)})
    if not proyecto:
        print(f"Proyecto con id {id_proyecto} no encontrado. calcularpftotal")
        return

    # Obtener los requerimientos del proyecto
    requerimientos = proyecto.get("Requerimientos", [])

    # Inicializar la suma total de PF
    pf_total = 0

    # Recorrer cada requerimiento y sumar los PF de sus componentes
    for req in requerimientos:
        componentes = req.get("Componentes", [])
        for componente in componentes:
            if componente.get("PF_own", 0) != "":
                print("componente posee pf modificado")
                pf_total += componente.get("PF_own", 0)
            else:
                print("pf automático")
                pf_total += componente.get("PF", 0)

    # Imprimir o retornar la suma total de PF
    print(f"La suma total de PF de todos los componentes en el proyecto {id_proyecto} es: {pf_total}")
    return pf_total
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