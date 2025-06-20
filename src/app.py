import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Character, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_CONNECTION_STRING")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API Star Wars funcionando 🚀"}), 200

# USERS
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    results = list(map(lambda u: u.serialize(), users))
    return jsonify(results), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        email=data.get("email"),
        password=data.get("password"),
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favs = Favorite.query.filter_by(user_id=user_id).all()
    results = list(map(lambda f: f.serialize(), favs))
    return jsonify(results), 200

# CHARACTERS
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    results = list(map(lambda c: c.serialize(), characters))
    return jsonify(results), 200

@app.route('/characters', methods=['POST']) 
def create_character():
    data = request.get_json()
    new_character = Character(
        name=data.get("name"),
        gender=data.get("gender"),
        birth_year=data.get("birth_year"),
        eye_color=data.get("eye_color")
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

# PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    results = list(map(lambda p: p.serialize(), planets))
    return jsonify(results), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    new_planet = Planet(
        name=data.get("name"),
        population=data.get("population"),
        climate=data.get("climate"),
        terrain=data.get("terrain")
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# FAVORITES
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    new_fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = request.json.get("user_id")
    new_fav = Favorite(user_id=user_id, character_id=character_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
