from flask import Flask, jsonify, request, render_template
import redis

# Initialiser l'application Flask
app = Flask(__name__)

# Connexion à Redis (assurez-vous que Redis fonctionne localement)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialiser des données d'exemple
if not r.exists("user_id_counter"):
    r.set("user_id_counter", 0)
r.hset('user:1', mapping={'name': 'Alice', 'age': '30', 'city': 'Paris'})
r.hset('user:2', mapping={'name': 'Bob', 'age': '25', 'city': 'Lyon'})
r.hset('user:3', mapping={'name': 'Lisa', 'age': '38', 'city': 'London'})

# Route pour ajouter un nouvel utilisateur
@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        # Récupérer les données envoyées dans la requête
        user_data = request.json
        
        # Vérifier les champs requis
        if not all(key in user_data for key in ("name", "age", "city")):
            return jsonify({"error": "Missing required fields: name, age, city"}), 400

        # Vérifier que l'âge est un entier positif
        if not str(user_data['age']).isdigit():
            return jsonify({"error": "Age must be a positive integer"}), 400

        # Générer un nouvel ID utilisateur
        user_id = r.incr("user_id_counter")

        # Ajouter les données dans Redis
        r.hset(f'user:{user_id}', mapping=user_data)

        return jsonify({"message": "User added successfully", "user_id": user_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer les données d'un utilisateur
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = r.hgetall(f'user:{user_id}')
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404

# Route pour afficher une page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
