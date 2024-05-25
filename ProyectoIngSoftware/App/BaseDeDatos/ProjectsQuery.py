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
    id_proyecto = 111 + user.BuscarProyectos(owner)

    db['Projects'].insert_one({'owner':owner,
                                'id':id_proyecto, 
                                'nombre':Nombre, 
                                "integrantes": integrantes, 
                                })

def BuscarProyecto(email_user, id_proyecto):
    '''Busca el proyecto en la base de datos'''
    if (db['Projects'].find_one({'email':email_user}) and db['Projects'].find_one({'id':id_proyecto}) != None):
        return True
    return False

def ObtenerDatosProyecto(email_user, id_proyecto):
    if BuscarProyecto(email_user, id_proyecto):
        nombre_proyecto = db['Projectos'].find_one({'email': email_user}, {'proyectos': 1})
        integrantes = 