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

    if not all_users:
        return ({"msg": "Users not found"}), 404

    users_serialized = list(map(lambda item : item.serialize(), all_users))

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

    if not all_planets:
        return ({"msg": "Planets not found"}), 404
    
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

    if not all_characters:
        return ({"msg": "Characters not found"}), 404

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

    if not all_vehicles:
        return ({"msg": "Vehicles not found"}), 404
    
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
    favorites = Favorites.query.filter_by(user_id=id).all()
    
    if not favorites:
        return jsonify({"msg": "No favorites found"}), 404

    # serializa cada favorito de la lista
    favorites_serialized = [favorite.serialize() for favorite in favorites]
    print(favorites_serialized)
    
    # mostrar resultados en response_body    
    response_body = {
        "msg": "Hello, this is your GET /vehicles response ",
        "results": favorites_serialized
    }

    return jsonify(response_body), 200


# *********** POSTS ***********

# Post user
@app.route('/user', methods=['POST'])
def add_user():

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a user"}), 400
    
    user = User.query.filter_by(email = data["email"]).first()

    if not user:
        new_user = User(
            email = data["email"], 
            user_name = data["user_name"],
            password = data["password"],
            is_active = data["is_active"]
            )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "user created successfully"}), 201  

    return jsonify({"msg": "user email already exists"}), 409

# Post planet
@app.route('/planet', methods=['POST'])
def add_planet():

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a planet"}), 400
    
    new_planet = Planet(
            name = data["name"],
            rotation_period = data["rotation_period"],
            orbital_period = data["orbital_period"],
            diameter = data["diameter"],
            climate = data["climate"],
            gravity = data["gravity"],
            terrain = data["terrain"],
            surface_water = data["surface_water"],
            population = data["population"]
            )
    
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Planet created successfully"}), 201

# Post character
@app.route('/character', methods=['POST'])
def add_character():

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a character"}), 400
    
    new_character = Character(
            name = data["name"],
            height = data["height"],
            mass = data["mass"],
            hair_color = data["hair_color"],
            skin_color = data["skin_color"],
            eye_color = data["eye_color"],
            birth_year = data["birth_year"],
            gender = data["gender"]
            )
    
    db.session.add(new_character)
    db.session.commit()

    return jsonify({"msg": "Character created successfully"}), 201

# Post vehicle
@app.route('/vehicle', methods=['POST'])
def add_vehicle():

    data = request.get_json()

    if not data:
        return jsonify({"msg": "You should specify a vehicle"}), 400
    
    new_vehicle = Vehicle(
            name = data["name"],
            model = data["model"],
            manufacturer = data["manufacturer"],
            cost_in_credits = data["cost_in_credits"],
            length = data["length"],
            max_atmosphering_speed = data["max_atmosphering_speed"],
            crew = data["crew"],
            passengers = data["passengers"],
            cargo_capacity = data["cargo_capacity"],
            consumables = data["consumables"],
            vehicle_class = data["vehicle_class"]
            )
    
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify({"msg": "Character created successfully"}), 201
   


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

# Delete an item on the favorite list of a specific user
@app.route('/favorite/<int:favoriteid>/<int:userid>', methods=['DELETE'])
def delete_planet_id(userid, favoriteid):

    user = User.query.filter_by(id=userid).first()

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorite_to_delete = Favorites.query.filter_by(id=favoriteid, user_id=userid).first()

    if favorite_to_delete is None:
        return jsonify({"msg": "Favorite not found"}), 404

    
    print(favorite_to_delete.serialize())
    
    db.session.delete(favorite_to_delete)
    db.session.commit()

    response_body = {
        "msg": "Favorite deleted"
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
