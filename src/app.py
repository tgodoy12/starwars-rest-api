"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Vehicle, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# ********** GET ***********

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():

    all_users = User.query.all()
    users_serialized = list(map(lambda item : item.serialize(), all_users))
    # print(users_serialized)

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": users_serialized
    }

    return jsonify(response_body), 200

# Get user by id
@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):

    user = User.query.filter_by(id=id).first()

    if user is None:
        return jsonify({"msg": "User not found"}), 404
    
    response_body = {
        "msg": "Hello, this is your GET /user/id response ",
        "result": user.serialize()
    }

    return jsonify(response_body), 200

# Get all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():

    all_planets = Planet.query.all()
    planets_serialized = list(map(lambda item : item.serialize(), all_planets))
    # print(planets_serialized)

    response_body = {
        "msg": "Hello, this is your GET /planets response ",
        "results": planets_serialized
    }

    return jsonify(response_body), 200

# Get all characters
@app.route('/characters', methods=['GET'])
def get_all_characters():

    all_characters = Character.query.all()
    characters_serialized = list(map(lambda item : item.serialize(), all_characters))
    # print(characters_serialized)

    response_body = {
        "msg": "Hello, this is your GET /characters response ",
        "results": characters_serialized
    }

    return jsonify(response_body), 200

# Get all vehicles
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    all_vehicles = Vehicle.query.all()
    vehicles_serialized = list(map(lambda item : item.serialize(), all_vehicles))
    

    response_body = {
        "msg": "Hello, this is your GET /vehicles response ",
        "results": vehicles_serialized
    }

    return jsonify(response_body), 200


# Get character by id
@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):

    character = Character.query.filter_by(id=id).first()

    if character is None:
        return jsonify({"msg": "Not found"}), 404
    
    character_serialized = character.serialize()
    # print(character)

    response_body = {
        "msg": "Hello, this is your GET /character/id response ",
        "result": character_serialized
    }

    return jsonify(response_body), 200

# Get planet by id
@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):

    planet = Planet.query.filter_by(id=id).first()
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    
    planet_serialized = planet.serialize()
    # print(planet)

    response_body = {
        "msg": "Hello, this is your GET /planet/id response ",
        "result": planet_serialized
    }

    return jsonify(response_body), 200

# Get vehicle by id
@app.route('/vehicle/<int:id>', methods=['GET'])
def get_one_vehicle(id):

    vehicle = Vehicle.query.filter_by(id=id).first()
    if vehicle is None:
        return jsonify({"msg": "Vehicle not found"}), 404
    
    vehicle_serialized = vehicle.serialize()
    # print(planet)

    response_body = {
        "msg": "Hello, this is your GET /vehicle/id response ",
        "result": vehicle_serialized
    }

    return jsonify(response_body), 200

# Get specific user's all favorites
@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_user_favorites(id):

    # obtención del usuario
    user = User.query.filter_by(id=id).first()

    if user is None:
        return jsonify({"msg": "User not found"}), 404
    
    user_serialized = user.serialize()
    print(user)
    
    # obtención de sus favoritos
    favorites = user.get_favorites()
    print(favorites)
    
    
    if not favorites:
        return jsonify({"msg": "No favorites found"}), 404

    # serialize() resultados
    # favorites_serialized = list(map(lambda item : item.serialize(), favorites))
    # print(favorites_serialized)
    
    # mostrar resultados en response_body    
    response_body = {
        "msg": "Hello, this is your GET /vehicles response ",
        "results": favorites
    }

    return jsonify(response_body), 200


# *********** POSTS ***********

# Post favorite planet for specific user
@app.route('/favorite/planet/<int:id>', methods=['POST'])
def add_favorite_planet(id):

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a user"}), 400
    
    user_id = data["user_id"]
    user = User.query.get(user_id)
    planet = Planet.query.get(id)

    # print(user, planet)

    if not user:
        return jsonify({"msg": "user not found"}), 404
    
    if not planet:
        return jsonify({"msg": "planet not found"}), 404
    

    favorite_planet = Favorites(user_id = data["user_id"], planet_id = id)
    db.session.add(favorite_planet)
    db.session.commit()
   
    response_body = {
        "msg": "Planet liked"
    }

    return jsonify(response_body), 201

# Post favorite character for specific user
@app.route('/favorite/character/<int:id>', methods=['POST'])
def add_favorite_character(id):

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a user"}), 400
    
    user_id = data["user_id"]
    user = User.query.get(user_id)
    character = Character.query.get(id)

    if not user:
        return jsonify({"msg": "user not found"}), 404
    
    if not character:
        return jsonify({"msg": "character not found"}), 404
    

    favorite_character = Favorites(user_id = data["user_id"], character_id = id)
    db.session.add(favorite_character)
    db.session.commit()
   
    response_body = {
        "msg": "Character liked"
    }

    return jsonify(response_body), 201

# Post favorite vehicle for specific user
@app.route('/favorite/vehicle/<int:id>', methods=['POST'])
def add_favorite_vehicle(id):

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a user"}), 400
    
    user_id = data["user_id"]
    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(id)

    if not user:
        return jsonify({"msg": "user not found"}), 404
    
    if not vehicle:
        return jsonify({"msg": "vehicle not found"}), 404
    

    favorite_vehicle = Favorites(user_id = data["user_id"], vehicle_id = id)
    db.session.add(favorite_vehicle)
    db.session.commit()
   
    response_body = {
        "msg": "Vehicle liked"
    }

    return jsonify(response_body), 201

# *********** DELETE ************


@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet_id(id):

    data = Planet.query.filter_by(id=id).first()

    if not data:
        return jsonify({"msg": "You should specify a planet to delete"}), 400
    
    print(data)
    
    # db.session.delete(data)
    # db.session.commit()

    response_body = {
        "msg": "Planet deleted"
    }

    return jsonify(response_body), 200









# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
