from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from users_db import leer_users, guardar_users
from backend import app
from db import guardar_json, leer_json
from werkzeug.security import generate_password_hash, check_password_hash
import requests

@app.route('/register', methods=['POST'])
@jwt_required()
def register():
    data = request.json
    usuario = data.get("username")
    contraseña = data.get("password")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("http://127.0.0.1:5000/login", headers = headers)
    guardar_users(usuario, contraseña)

@app.route('/usuario' , methods=['GET'])
@jwt_required()
def users():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("http://127.0.0.1:5000/login", headers = headers)
    print(leer_users())

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    users = leer_users()

    # usuario no existe
    if username not in users:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # contraseña incorrecta
    if not check_password_hash(users[username], password):
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify({"access_token":access_token}),200


