from flask import Flask, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'mi_clave_secreta_jwt'

# Simulación de una base de datos (deberías usar una base de datos real)
users_db = []

# Variable global para almacenar el token
global_token = None

# Simulación de una lista de tokens revocados
revoked_tokens = set()

def verify_token(token):
    if token in revoked_tokens:
        return False
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded['username']
    except jwt.ExpiredSignatureError:
        return 'Token expirado'
    except jwt.InvalidTokenError:
        return 'Token inválido'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    username = data.get('username')
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    password = data.get('password')
    telefono = data.get('telefono')

    if not username or not email or not nombre or not apellido or not password or not telefono:
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    if any(user['username'] == username for user in users_db):
        return jsonify({'message': 'Nombre de usuario ya existe'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    user = {
        'username': username,
        'email': email,
        'nombre': nombre,
        'apellido': apellido,
        'password': hashed_password,
        'telefono': telefono
    }

    users_db.append(user)

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    username = data.get('username')
    password = data.get('password')

    user = next((u for u in users_db if u['username'] == username), None)

    try:
        if user is not None and check_password_hash(user['password'], password):
            token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
            
            global_token = token

            datos_usuario = {
                'username': user['username'],
                'email': user['email'],
                'nombre': user['nombre'],
                'apellido': user['apellido'],
                'telefono': user['telefono']
            }       

            return jsonify({'token': global_token ,'user': datos_usuario}), 200
            
        else:
            print(f"Error en el inicio de sesión para el usuario {username}")
            return jsonify({'message': 'Credenciales inválidas'}), 401
    
    except Exception as e:
        print(f"Error durante el inicio de sesión: {str(e)}")
        return jsonify({'message': f'Error interno durante el inicio de sesión: {str(e)}'}), 500

@app.route('/users', methods=['GET'])
def get_users():
    global global_token
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token no proporcionado'}), 401

    username = verify_token(token)
    
    if not username:
        return jsonify({'message': 'Token inválido o expirado'}), 401

    # Configura el token en las solicitudes a otras rutas
    global_token = token

    return jsonify({'users': users_db}), 200

@app.route('/logout', methods=['POST'])
def logout():
    global global_token
    if global_token:
        revoked_tokens.add(global_token)  # Agrega el token a la lista de revocados
        global_token = None
        return jsonify({'message': 'Logout exitoso'}), 200
    else:
        return jsonify({'message': 'No hay sesión activa'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)