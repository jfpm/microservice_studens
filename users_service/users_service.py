from flask import Flask, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # Importa la extensión

app = Flask(__name__)
CORS(app)  # Configura CORS para la aplicación
app.config['SECRET_KEY'] = 'mi_clave_secreta_jwt'

# Simulación de una base de datos (deberías usar una base de datos real)
users_db = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    password = data.get('password')
    telefono = data.get('telefono')

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
    username = data.get('username')
    password = data.get('password')
    
    user = next((u for u in users_db if u['username'] == username), None)
    try:
        if user and check_password_hash(user['password'], password):
            token = jwt.encode({'username': username}, app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')}), 200
        else:
            print(f"Error en el inicio de sesión para el usuario {username}")
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        print(f"Error durante el inicio de sesión: {str(e)}")
        return jsonify({'message': 'Error interno durante el inicio de sesión'}), 500




@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': users_db}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
