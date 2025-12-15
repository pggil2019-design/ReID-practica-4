from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import guardar_mensaje_db, cargar_mensajes, modificar_mensaje_db, borrar_mensaje_db
from schemas import MessageSchema

texts_bp = Blueprint('texts', __name__)

@texts_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    data = request.json
    try:
        MessageSchema().load(data) # Espera campo "sentence"
    except:
        return jsonify({"error": "Falta 'sentence'"}), 400
        
    msg_id = guardar_mensaje_db(data['sentence'])
    return jsonify({"message": "Mensaje guardado", "id": msg_id}), 201

@texts_bp.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(cargar_mensajes()), 200

@texts_bp.route('/modify/<msg_id>', methods=['PUT'])
@jwt_required()
def modify_message(msg_id):
    data = request.json
    if modificar_mensaje_db(msg_id, data.get('sentence')):
        return jsonify({"message": "Actualizado"}), 200
    return jsonify({"error": "Mensaje no encontrado"}), 404

@texts_bp.route('/delete/<msg_id>', methods=['DELETE'])
@jwt_required()
def delete_message(msg_id):
    if borrar_mensaje_db(msg_id):
        return jsonify({"message": "Eliminado"}), 200
    return jsonify({"error": "Mensaje no encontrado"}), 404