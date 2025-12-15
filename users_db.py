import json
import os

FILE_USERS="users.json"

def cargar_datos():
    with open(FILE_USERS, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return {}

def guardar_usuario_db(username, password, is_admin=False):
    datos=cargar_datos()
    datos[username]= {
        "password": password,
        "is_admin": is_admin
    }
    with open(FILE_USERS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

def leer_users(username):
    datos=cargar_datos()
    return datos.get(username)

def hacer_admin(username):
    datos = cargar_datos()
    if username in datos:
        datos[username]["is_admin"] = True
        with open(FILE_USERS, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4)
        return True
    return False