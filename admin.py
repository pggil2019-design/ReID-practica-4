from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash
from users_db import guardar_usuario_db, leer_users, hacer_admin

admin_bp = Blueprint('admin', __name__)

# Endpoint /admin/register: Crea un usuario que YA es administrador directamente
@admin_bp.route('/register', methods=['POST'])
def register_admin():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if leer_users(username):
        return jsonify({"error": "Usuario ya existe"}), 400

    hashed_pw = generate_password_hash(password)
    #Almacena usuario como admin=True
    guardar_usuario_db(username, hashed_pw, is_admin=True)
    return jsonify({"message": "Admin registrado"}), 201

# Endpoint /admin/grant: Convierte un usuario normal en admin
@admin_bp.route('/grant', methods=['PUT'])
@jwt_required()
def grant_admin_privileges():
    # Solo puede ser ejecutado por administradores
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"error": "Acceso denegado. Se requiere ser admin"}), 403

    data = request.json
    target_user = data.get("username")
    
    if hacer_admin(target_user):
        return jsonify({"message": f"{target_user} ahora es admin"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Endpoint /admin/status/<id>: Verifica si es admin
@admin_bp.route('/status/<username>', methods=['GET'])
def check_status(username):
    user_data = leer_users(username)
    if user_data:
        return jsonify({"username": username, "is_admin": user_data["is_admin"]}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404