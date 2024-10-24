from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from bs_db_manager import DBManager


manager = DBManager()
app = Flask(__name__)

User = Query()
db = manager.db

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()  
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({"error": "Invalid data"}), 400

    db.insert(data)  
    return jsonify({"message": "User added successfully", "user": data}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = db.table('user').all()     
    return jsonify({"users": users}), 200


@app.route('/users/<gametag>', methods=['GET'])
def get_user(gametag):
    user_data =  db.table('user').search(User.gametag == gametag)  
    if not gametag:
        return jsonify({"error": "User not provided"}), 404
    
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    print(user_data)
    
    return jsonify({"user": user_data[0]}), 200


if __name__ == '__main__':
    app.run(debug=True)
