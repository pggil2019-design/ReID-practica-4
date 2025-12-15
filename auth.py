from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from users_db import guardar_usuario_db, leer_users, cargar_datos
from schemas import UserSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    # Validación básica Marshmallow
    try:
        UserSchema().load(data)
    except:
        return jsonify({"error": "Datos inválidos"}), 400

    username = data.get("username")
    password = data.get("password")
    
    if leer_users(username):
        return jsonify({"error": "Usuario ya existe"}), 400

    # Guardar con hash y por defecto NO admin
    hashed_pw = generate_password_hash(password)
    guardar_usuario_db(username, hashed_pw, is_admin=False)
    
    return jsonify({"message": "Usuario registrado"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    user_data = leer_users(username) # {password: "...", is_admin: ...}
    
    if not user_data or not check_password_hash(user_data['password'], password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    # Creamos token. Podemos guardar si es admin en el token si queremos.
    access_token = create_access_token(identity=username, additional_claims={"is_admin": user_data['is_admin']})
    return jsonify({"access_token": access_token}), 200

@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(cargar_datos()), 200