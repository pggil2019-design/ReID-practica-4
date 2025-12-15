from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from db import guardar_json, leer_json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

#GET endpoint
@app.route('/hello' , methods=['GET'])
def hello_world():
    return "hello world", 200

#POST endpoint
@app.route('/echo', methods=['POST'])
def echo_sentence():
    data = request.get_json()

    if not data or "sentence" not in data:
        return jsonify({"error": "Missing 'sentence' field"}), 400

    return jsonify({"echo": data["sentence"]}), 200

#POST endpoint
@app.route('/usuario', methods=['POST'])
def echo_usuario():
    data = request.get_json()

    if not data or "nombre" not in data or "edad" not in data:
        return jsonify({"error": "Missing 'nombre' field"}), 400

    guardar_json(data)

    return jsonify({data["id"]:{"id":data["id"],"nombre":data["nombre"],"edad":data["edad"]}}), 200


if __name__ == '__main__':
    app.run(debug=True)
