from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mi_base_de_datos']

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    username = request.args.get('username')

    user_data = db.users.find_one({'username': username}, {'_id': 0})
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

if __name__ == '__main__':
    app.run(port=5001)
