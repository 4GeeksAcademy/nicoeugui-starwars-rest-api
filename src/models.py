from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '{}'.format(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, it's a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }

class FavoritePlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_relationship = db.relationship(Users)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet_relationship = db.relationship(Planets)

    def __repr__(self):
        return '{} {}'.format(self.user_id, self.planet_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet_relationship.serialize() if self.planet_relationship else None
        }



class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    height = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet_relationship = db.relationship(Planets)
    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "is_active": self.is_active,
            "planet_id": self.planet_id,
            # do not serialize the password, its a security breach
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_relationship = db.relationship(Users)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people_relationship = db.relationship(People)

    def __repr__(self):
        return '{} {}'.format(self.user_id, self.people_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_email": self.user_relationship.email,
            "people_name": self.people_relationship.name,
            # do not serialize the password, it's a security breach
        }


class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '{} {}'.format(self.name, self.model)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            # do not serialize the password, its a security breach
        }

class VehiclesPilots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people_relationship = db.relationship(People)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle_relationship = db.relationship(Vehicles)


class FavoriteVehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_relationship = db.relationship(Users)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle_relationship = db.relationship(Vehicles)

    def __repr__(self):
        return '{} {}'.format(self.user_id, self.vehicle_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_email": self.user_relationship.email,
            "vehicle_id": self.vehicle_relationship.name,
        }
