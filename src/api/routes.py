"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Listar usuarios
@api.route('/users', methods=['GET'])
def list_users():

    users = User.query.all()

    if not users:
        return jsonify({ "msg": "Users not found"}), 404

    response_body = [user.serialize() for user in users]

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def form_signup():
    first_name = request.json.get("first_name", '')
    last_name = request.json.get("last_name", '')
    email = request.json.get("email")
    password = request.json.get("password")
    
    # Verificar si el usuario ya existe
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "El email ya está registrado"}), 401
    
    # Crear nuevo usuario
    hashed_password = generate_password_hash(password)
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email, 
        password=hashed_password
    )
    
    # Intentaremos añadir el usuario con try/except
    try:
        db.session.add(new_user)
        db.session.commit()
    
        return jsonify({"msg": "Usuario creado exitosamente"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 500

@api.route('/login', methods=['POST'])
def form_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email=email).first()
    
    # Verificar si existe el usuario y la contraseña es correcta
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Email o contraseña incorrectos"}), 401
    
    # Si surge error al iniciar sesion, usaremos try/except
    try:
        # Crear token JWT
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token, "user_id": user.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al iniciar sesion: {str(e)}"}), 500

@api.route('/private', methods=['GET'])
@jwt_required()
def form_private():
    # Acceder a la identidad del usuario actual con get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({"isAuthenticated": True, "user": user.serialize()}), 200
