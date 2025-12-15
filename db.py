import json
import uuid

FILE_MESSAGES="messages.json"


def cargar_mensajes():
    try:
        with open(FILE_MESSAGES, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                return {}
    except FileNotFoundError:
        return {}

def guardar_mensaje_db(texto):
    datos = cargar_mensajes()
    msg_id = uuid.uuid4().hex # Generar ID único
    datos[msg_id] = texto
    with open(FILE_MESSAGES, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)
    return msg_id

def modificar_mensaje_db(msg_id, nuevo_texto):
    datos = cargar_mensajes()
    if msg_id in datos:
        datos[msg_id] = nuevo_texto
        with open(FILE_MESSAGES, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4)
        return True
    return False

def borrar_mensaje_db(msg_id):
    datos = cargar_mensajes()
    if msg_id in datos:
        del datos[msg_id]
        with open(FILE_MESSAGES, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4)
        return True
    return False