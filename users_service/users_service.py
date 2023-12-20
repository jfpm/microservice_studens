from flask import Flask, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'mi_clave_secreta_jwt'

# Simulación de una base de datos (deberías usar una base de datos real)
# Conexión a la base de datos MySQL

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
    perfil = 1

    if not username or not email or not nombre or not apellido or not password or not telefono:
        return jsonify({'message': 'Todos los campos son obligatorios'}), 401
    
    connection = pymysql.connect(host='mysql', user='adminroot', password='rootroot1', db='userdb')

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE username=%s"
            cursor.execute(sql,(username))
            existing_user = cursor.fetchone()

            if existing_user is not None:
                return jsonify({'message': 'Nombre de usuario ya existe'}), 401

            hashed_password = generate_password_hash(password, method='sha256')

            cursor.execute(
                "INSERT INTO usuarios (username, email, nombre, apellido, password, telefono, perfil) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (username, email, nombre, apellido, hashed_password, telefono, perfil)
            )

            connection.commit()

            return jsonify({'message': 'Usuario registrado exitosamente'}), 201
            
    except Exception as e:
        print(f"Error durante el registro: {str(e)}")
        return jsonify({'message': f'Error interno durante el registro: {str(e)}'}), 500
    
    finally:
            connection.close()
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400
    
    connection = pymysql.connect(host='mysql', user='adminroot', password='rootroot1', db='userdb')

    username = data.get('username')
    password = data.get('password')

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE username=%s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()

        if user is not None and check_password_hash(user[5], password):  
            token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
            
            global_token = token

            datos_usuario = {
                'username': user[1],  
                'email': user[2],
                'nombre': user[3],
                'apellido': user[4],
                'telefono': user[6],
                'perfil': user[7]
            }       

            return jsonify({'token': global_token ,'user': datos_usuario}), 200
            
        else:
            print(f"Error en el inicio de sesión para el usuario {username}")
            return jsonify({'message': 'Credenciales inválidas'}), 401
    
    except Exception as e:
        print(f"Error durante el inicio de sesión: {str(e)}")
        return jsonify({'message': f'Error interno durante el inicio de sesión: {str(e)}'}), 500
    
    finally:
        connection.close()


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

    connection = pymysql.connect(host='mysql', user='adminroot', password='rootroot1', db='userdb')

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)

            # Obtener los nombres de las columnas
            column_names = [column[0] for column in cursor.description]

            users = cursor.fetchall()

            user_list = []
            for user in users:
                user_data = {column: user[column_names.index(column)] for column in column_names if column != 'password'}
                user_list.append(user_data)

            return jsonify({'users': user_list}), 200

    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")
        return jsonify({'message': f'Error interno al obtener usuarios: {str(e)}'}), 500

    finally:
        connection.close()



@app.route('/logout', methods=['POST'])
def logout():
    global global_token
    if global_token:
        revoked_tokens.add(global_token)  # Agrega el token a la lista de revocados
        global_token = None
        return jsonify({'message': 'Logout exitoso'}), 200
    else:
        return jsonify({'message': 'No hay sesión activa'}), 400


#Perfiles 
# Profile methods
def register_profile(name, ind_estado, created_by):
    profile = {
        'id': len(profiles_db) + 1,
        'name': name,
        'ind_estado': ind_estado,
        'created_at': str(datetime.datetime.now()),
        'created_by': created_by
    }
    profiles_db.append(profile)
    return profile

def get_profiles():
    return profiles_db

def update_profile(profile_id, name, ind_estado, created_by):
    for profile in profiles_db:
        if profile['id'] == profile_id:
            profile['name'] = name
            profile['ind_estado'] = ind_estado
            profile['created_by'] = created_by
            return profile
    return None

def enable_disable_profile(profile_id, enable):
    for profile in profiles_db:
        if profile['id'] == profile_id:
            profile['ind_estado'] = 1 if enable else 0
            return profile
    return None

def count_users_by_profile(profile_id):
    count = sum(1 for user in users_db if user['profile_id'] == profile_id)
    return count

# Profile registration route
@app.route('/profiles', methods=['POST'])
def register_profile_route():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    name = data.get('name')
    ind_estado = data.get('ind_estado', 1)  # Default to active
    created_by = data.get('created_by')

    if not name or not created_by:
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    profile = register_profile(name, ind_estado, created_by)

    return jsonify({'message': 'Perfil registrado exitosamente', 'profile': profile}), 201

# Get profiles route
@app.route('/profiles', methods=['GET'])
def get_profiles_route():
    profiles = get_profiles()
    return jsonify({'profiles': profiles}), 200

# Update profile route
@app.route('/profiles/<int:profile_id>', methods=['PUT'])
def update_profile_route(profile_id):
    data = request.get_json()
    # Existing code...

# Enable/disable profile route
#@app.route('/profiles/<int:profile_id>/<string:action>', methods=['PUT'])
#def enable_disable_profile_route(profile_id, action):
    # Existing code...

# Ruta para contar usuarios por perfil
@app.route('/profiles/<int:profile_id>/users', methods=['GET'])
def contar_usuarios_por_perfil(profile_id):
    count = count_users_by_profile(profile_id)
    return jsonify({'cantidad_usuarios': count}), 200 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)