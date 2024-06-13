from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.UsersQuery as user
import BaseDeDatos.ProjectsQuery as Proj
from pymongo import MongoClient, errors
from datetime import date

def AgregarRequerimientos(id_proyecto:int, member:list, requesNcomp:list):
    """
    Función para agregar requerimientos a\nun proyecto existente.
    
    requesNcomp --> [ (Requerimiento, [ componentes ] ) ]
    id_proyecto --> ObjectId de MongoDB
    member --> [ (correo_miembro, rol) ]
    """

    #Falta agregar lógica para asignar a usuarios a estimar un requerimiento

    lista_de_requerimientos = [] #Lista que contiene cada requerimiento con sus datos.
    lista_de_componentes = [] #Lista que contiene cada componente de un requerimiento.
    id = 1

    reques_W_id = [] #Creamos una lista nueva de requerimientos con un id
    for req in requesNcomp:
        reques_W_id.append([id,req])
        id +=1
    """
    reques_W_id --> [  ]
    """

    requerimiento = {
        "ID" : int,
        "Asignado" : None,
        "Descripción" : str,
        "FechaAsignación" : date.today(),
        "Estimado" : bool,
        "Componentes" : lista_de_componentes
    }
    Componente = { #Descripción, Tipo, atributos, PF, own y razón vendrán desde la query para agregar en la ventana de desarrollador.
        "ID" : int,
        "Descripcion" : str,
        "Tipo" : int, #in (0,1,2,3,4)
        "Atributos" : int,
        "PF" : int, #automático desde atributos
        "PF_own" : (bool,int),
        "Razon" : str
    }

    """Agregamos cada requerimiento como un diccionario en una lista
    
            Requerimiento = {
                        "ID" = 0,
                        "Asignado" = "prueba@gmail.com,
                        "Descripción" = Lorem Ipsum,
                        "FechaAsignación" = date.today(),
                        "Estimado" = False,
                        "Componentes" = [
                                        "ID" = 0,
                                        "Descripcion" = "Ingresar datos de usuario.",
                                        "Tipo" = 3,
                                        "Atributos" = 5, 
                                        "PF" = x,
                                        "PF_own" = (False, None),
                                        "Razon" = None
                                        ]
                            }
    """
    for req in reques_W_id:
        id = 0
        id_req = req[0]
        descripcion = req[1][0]
        componentes = req[1][1]
        requerimiento["ID"] = id_req
        requerimiento["Asignado"] = None
        requerimiento["Descripción"] = descripcion
        requerimiento["FechaAsignación"] = date.today()
        requerimiento["Estimado"] = False
        if componentes == []:
            pass
        else:
            j = 0
            for comp in componentes:
                Componente["ID"] = j
                Componente["Descripcion"] = comp
                Componente["Tipo"] = int
                Componente["Atributos"] = int
                Componente["PF"] = None
                Componente["PF_own"] = None
                Componente["Razon"] = None
                lista_de_componentes.append(Componente)
                j+=1

        requerimiento["Componentes"] = lista_de_componentes

        lista_de_requerimientos.append(requerimiento)
    

    puntos_de_funcion_totales = 0
    for req in lista_de_requerimientos:#iteramos sobre un diccionario
        compo = req["Componentes"]#es una lista
        for dicc in compo:
            pf = dicc["PF"]
            if pf == None:
                break
            else:
                puntos_de_funcion_totales += pf

    query = {
        "id_proyecto": id_proyecto,#id de mongoDB. Acá se asocia el proyecto para los requerimientos
        "Requerimientos": lista_de_requerimientos,
        "TotalPF" : puntos_de_funcion_totales
    }

    try : 
        db["ReqComp"].insert_one(query)
        print("Requerimientos agregados con éxito")
    except Exception as e:
        print("Ocurrió un error")


    


def AgregarComponentes(id_proyecto):
    return

def ObtenerRequerimientos(email, id_proyecto):
    return