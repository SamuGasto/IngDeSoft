from BaseDeDatos.MainMongoDB import db
from bson.objectid import ObjectId

def TextoTablaVAC(texto: str,indice: int) -> str:
    return db['DefaultValues'].find_one({'_id':ObjectId('6644231fd5afbadaf36fcd24')})[texto][indice]