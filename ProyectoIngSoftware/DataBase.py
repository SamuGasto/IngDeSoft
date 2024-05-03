import pyodbc
import pandas as pd

server = 'LAPTOP-KHL9HM6I\INGDESOFT'
bd = 'master'
user = 'ingDeSoft02024'
password = 'Panconqueso'
port = '5273'

conn = 0
cursor = 0

def ConectarBaseDeDatos():
    try:
        global conn, cursor
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={bd};UID={user};PWD={password}'
        conn = pyodbc.connect(connectionString) 
        cursor = conn.cursor()
        print('Conexión exitosa')
    except:
        print('Error al conectar')

def CerrarCursor():
    global cursor
    cursor.close()

def ListaTablas():
    sqlQuery = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
    rows = cursor.execute(sqlQuery).fetchall()
    for r in rows:
        print(r)
    CerrarCursor()

def AgregarUsuario(email,password):
    global conn, cursor
    sqlQuery = '''
    INSERT INTO Users 
    VALUES (1, 'samuel.55321@gmail.com', 'tomate';)
    '''
    cursor.execute(sqlQuery)
    conn.commit()
    CerrarCursor()

def EliminarUsuarios():
    global conn, cursor
    sqlQuery = '''
    DELETE FROM Users;
    '''
    cursor.execute(sqlQuery)
    conn.commit()
    CerrarCursor()

def ListaUsuarios():
    global cursor
    sqlQuery = '''
    SELECT * FROM Users;
    '''
    rows = cursor.execute(sqlQuery).fetchall()
    return rows




