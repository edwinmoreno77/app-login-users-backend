from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import User
import re
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS basic configuration
    CORS(app, 
         resources={r"/*": {
             "origins": [
                 os.getenv('FRONTEND_URL', 'http://localhost:5173'),
                 'https://app-login-users.vercel.app'
             ],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "max_age": 3600
         }}
    )
    
    # JWT configuration
    jwt = JWTManager(app)

    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_password(password):
        return len(password) >= 6

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.json
        
        if not all([data.get('name'), data.get('email'), data.get('password')]):
            return jsonify({'message': 'Todos los campos son obligatorios'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'message': 'Formato de correo electrónico inválido'}), 400
        
        if not validate_password(data['password']):
            return jsonify({'message': 'La contraseña debe tener al menos 6 caracteres'}), 400

        if User.get_by_email(data['email']):
            return jsonify({'message': 'El correo electrónico ya está registrado'}), 409

        try:
            user = User(
                name=data['name'],
                email=data['email'],
                profile={
                    'avatar': data.get('avatar'),
                    'phone': data.get('phone'),
                    'address': data.get('address')
                }
            )
            user.set_password(data['password'])
            user.save()
            
            token = create_access_token(identity=str(user.id))
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'token': token,
                'user': user.to_public_dict()
            }), 201

        except Exception as e:
            print(f"Error al registrar usuario: {str(e)}")  # Add log for debugging
            return jsonify({'message': 'Error al registrar usuario', 'error': str(e)}), 500

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        
        if not all([data.get('email'), data.get('password')]):
            return jsonify({'message': 'Email y contraseña son requeridos'}), 400

        user = User.get_by_email(data['email'])
        
        if user and user.check_password(data['password']):
            if not user.is_active:
                return jsonify({'message': 'Cuenta desactivada'}), 403
                
            user.update_last_login()
            token = create_access_token(identity=str(user.id))
            return jsonify({
                'message': 'Login exitoso',
                'token': token,
                'user': user.to_public_dict()
            }), 200
        
        return jsonify({'message': 'Credenciales inválidas'}), 401

    @app.route('/api/users/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        return jsonify(user.to_dict()), 200

    @app.route('/api/users', methods=['GET'])
    @jwt_required()
    def get_users():
        try:
            # Get the current user to verify permissions
            current_user_id = get_jwt_identity()
            current_user = User.get_by_id(current_user_id)
            
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado'}), 404
                
            # Get all active users
            users = User.objects(is_active=True).order_by('-created_at')
            
            # Convert to list of dictionaries
            users_list = [user.to_public_dict() for user in users]
            
            return jsonify({
                'users': users_list,
                'total': len(users_list)
            }), 200
            
        except Exception as e:
            print(f"Error al obtener usuarios: {str(e)}")  # Add log for debugging
            return jsonify({
                'message': 'Error al cargar los usuarios',
                'error': str(e)
            }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port, debug=False)