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
from models import db, Users, People, Planets, Vehicles, VehiclesPilots, FavoritePeople, FavoritePlanets, FavoriteVehicles
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

@app.route('/users', methods=['GET'])
def get_users():

    users = Users.query.all()
    serialized_users = list(map(lambda item: item.serialize(), users))

    return jsonify({'msg': 'ok', 'results': serialized_users}), 200

@app.route('/people', methods=['GET'])
def get_people():

    people = People.query.all()
    serialized_people = list(map(lambda item: item.serialize(), people))

    return jsonify({'msg': 'ok', 'results': serialized_people}), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_for_id(people_id):

    people = People.query.get(people_id)
    serialized_people = people.serialize()

    return jsonify({'msg': 'ok', 'results': serialized_people}), 200


@app.route('/planet', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    serialized_planets = list(map(lambda item: item.serialize(), planets))

    return jsonify({'msg': 'ok', 'results': serialized_planets}), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planets_id(planet_id):

    planet = Planets.query.get(planet_id)
    serialized_planets = planet.serialize()

    return jsonify({'msg': 'ok', 'results': serialized_planets}), 200

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_users_favorites(user_id):

    user = Users.query.get(user_id)

    serialized_user = user.serialize()

    favorite_people = FavoritePeople.query.filter_by(user_id=user_id).all()
    favorite_planets = FavoritePlanets.query.filter_by(user_id=user_id).all()
    favorite_vehicles = FavoriteVehicles.query.filter_by(user_id=user_id).all()

    serialized_people = list(map(lambda item: item.serialize(), favorite_people))
    serialized_planets = list(map(lambda item: item.serialize(), favorite_planets))
    serialized_vehicles = list(map(lambda item: item.serialize(), favorite_vehicles))

    return jsonify({'msg': 'ok', 'user': serialized_user, 'favorite_people': serialized_people, 
                    'favorite_planets': serialized_planets, 
                    'favorite_vehicles': serialized_vehicles}), 200

@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    request_body = request.get_json(silent=True)

    user_id = request_body.get('user_id')
    user = Users.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if user is None:
        return jsonify({"msg": f"El usuario con id {user_id} no existe"}), 400

    if planet is None:
        return jsonify({"msg": f"El planeta con id {planet_id} no existe"}), 400

    
    existing_favorite = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"msg": f"El planeta ya está en la lista de favoritos del usuario"}), 400

    favorite_planet = FavoritePlanets()
    favorite_planet.user_id = user_id
    favorite_planet.planet_id = planet_id
    favorite_planet.planet = planet
    db.session.add(favorite_planet)
    db.session.commit()

    favorite_people_query = FavoritePeople.query.filter_by(user_id=user_id)
    serialized_favorite_people = list(map(lambda item: item.serialize(), favorite_people_query))

    favorite_planets_query = FavoritePlanets.query.filter_by(user_id=user_id)
    serialized_favorite_planets = list(map(lambda item: item.serialize(), favorite_planets_query))

    response_body = {
        "msg": "ok",
        "total_favorites": len(serialized_favorite_people) + len(serialized_favorite_planets),
        "results": {
            "favorite_people": serialized_favorite_people,
            "favorite_planets": serialized_favorite_planets
        }
    }

    return jsonify(response_body)


@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):

    request_body = request.get_json(silent=True)

    user_id = request_body.get('user_id')
    user = Users.query.get(user_id)
    people = People.query.get(people_id)

    if user is None:
        return jsonify({"msg": f"El usuario con id {user_id} no existe"}), 400

    if people is None:
        return jsonify({"msg": f"El planeta con id {people_id} no existe"}), 400

    
    existing_favorite = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    if existing_favorite:
        return jsonify({"msg": f"El planeta ya está en la lista de favoritos del usuario"}), 400

    favorite_people = FavoritePeople()
    favorite_people.user_id = user_id
    favorite_people.people_id = people_id
    favorite_people.people = people
    db.session.add(favorite_people)
    db.session.commit()

    favorite_people_query = FavoritePeople.query.filter_by(user_id=user_id)
    serialized_favorite_people = list(map(lambda item: item.serialize(), favorite_people_query))

    response_body = {
        "msg": "ok",
        "total_favorites": len(serialized_favorite_people),
        "results": {
            "favorite_people": serialized_favorite_people,
        }
    }

    return jsonify(response_body)

@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    request_data = request.get_json(silent=True)

    if not request_data or 'user_id' not in request_data:
        return jsonify({"msg": "Se requiere 'user_id' en el cuerpo JSON"}), 400

    user_id = request_data['user_id']
    favorite_planet = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if favorite_planet:
        db.session.delete(favorite_planet)
        db.session.commit()

        return jsonify({"msg": f"Planeta con ID {planet_id} eliminado de los favoritos"}), 200
    else:
        return jsonify({"msg": f"El planeta con ID {planet_id} no está en la lista de favoritos del usuario"}), 404

@app.route('/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    request_data = request.get_json(silent=True)

    if not request_data or 'user_id' not in request_data:
        return jsonify({"msg": "Se requiere 'user_id' en el cuerpo JSON"}), 400

    user_id = request_data['user_id']
    favorite_people = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()

    if favorite_people:
        db.session.delete(favorite_people)
        db.session.commit()

        return jsonify({"msg": f"People con ID {people_id} eliminado de los favoritos"}), 200
    else:
        return jsonify({"msg": f"El People con ID {people_id} no está en la lista de favoritos del usuario"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
