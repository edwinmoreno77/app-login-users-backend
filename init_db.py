from app import create_app
from models import User

def init_db():
    app = create_app()
    with app.app_context():
        # Limpiar la colección de usuarios
        User.objects.delete()
        
        # Crear usuarios de prueba
        users = [
            {
                'name': 'Usuario 1',
                'email': 'usuario1@example.com',
                'password': 'user123'
            },
            {
                'name': 'Usuario 2',
                'email': 'usuario2@example.com',
                'password': 'user123'
            }
        ]
        
        for user_data in users:
            user = User(
                name=user_data['name'],
                email=user_data['email']
            )
            user.set_password(user_data['password'])
            user.save()
            print(f"Usuario creado: {user.email}")

if __name__ == '__main__':
    init_db() 