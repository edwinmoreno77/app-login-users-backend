from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import User
import re

auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json
    
    if not all([data.get('name'), data.get('email'), data.get('password')]):
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400
    
    if not validate_email(data['email']):
        return jsonify({'message': 'Formato de correo electrónico inválido'}), 400
    
    if not validate_password(data['password']):
        return jsonify({'message': 'La contraseña debe tener al menos 6 caracteres'}), 400

    if User.objects(email=data['email']).first():
        return jsonify({'message': 'El correo electrónico ya está registrado'}), 409

    try:
        user = User(
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.save()
        
        token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'token': token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'message': 'Error al registrar usuario', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json
    
    if not all([data.get('email'), data.get('password')]):
        return jsonify({'message': 'Email y contraseña son requeridos'}), 400

    user = User.objects(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': user.to_dict()
        }), 200
    
    return jsonify({'message': 'Credenciales inválidas'}), 401

@users_bp.route('/', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_users():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        users = User.objects.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'message': 'Error al obtener usuarios', 'error': str(e)}), 500

@users_bp.route('/<id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_user_by_id(id):
    if request.method == 'OPTIONS':
        return '', 200
        
    user = User.objects(id=id).first()
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    return jsonify({
        'status': 'Success',
        'data': user.to_dict()
    }), 200 