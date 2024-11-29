from flask import Flask, jsonify, request
import redis

# Initialiser l'application Flask
app = Flask(_name_)

# Connexion à Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Route pour la racine
@app.route('/')
def home():
    return "Bienvenue dans l'API Flask avec Redis."

# Route pour ajouter un utilisateur
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("id", "name", "age", "city")):
        return jsonify({"error": "Invalid data"}), 400
    user_id = data["id"]
    r.hset(f"user:{user_id}", mapping={
        "name": data["name"],
        "age": data["age"],
        "city": data["city"]
    })
    return jsonify({"message": f"User {user_id} added successfully."}), 201

# Route pour récupérer un utilisateur
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = r.hgetall(f"user:{user_id}")
    if user_data:
        user_data = {key.decode(): value.decode() for key, value in user_data.items()}
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404

# Lancer l'application Flask
if _name_ == '_main_':
    app.run(debug=True)