#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

# Root route
@app.route('/')
def index():
    return '<h1>Superheroes API</h1>'

# a. GET /heroes
class HeroesResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        # Serialize only id, name, and super_name as per requirements
        hero_dicts = [
            {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
            for hero in heroes
        ]
        return make_response(jsonify(hero_dicts), 200)

api.add_resource(HeroesResource, '/heroes')

# b. GET /heroes/:id
class HeroByIdResource(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if not hero:
            return make_response(jsonify({"error": "Hero not found"}), 404)
        
        # Manually constructing the response to match the exact specified format
        # including nested power details within hero_powers
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": []
        }
        
        for hero_power in hero.hero_powers:
            # Get the associated power and serialize it
            power_data = hero_power.power.to_dict(rules=('-hero_powers',)) # Exclude hero_powers from power
            hero_power_entry = {
                "id": hero_power.id,
                "hero_id": hero_power.hero_id,
                "power_id": hero_power.power_id,
                "strength": hero_power.strength,
                "power": {
                    "description": power_data.get('description'),
                    "id": power_data.get('id'),
                    "name": power_data.get('name')
                }
            }
            hero_dict['hero_powers'].append(hero_power_entry)
        
        return make_response(jsonify(hero_dict), 200)

api.add_resource(HeroByIdResource, '/heroes/<int:id>')

# c. GET /powers
class PowersResource(Resource):
    def get(self):
        powers = Power.query.all()
        # Serialize only id, name, and description as per requirements
        power_dicts = [
            {"description": power.description, "id": power.id, "name": power.name}
            for power in powers
        ]
        return make_response(jsonify(power_dicts), 200)

api.add_resource(PowersResource, '/powers')

# d. GET /powers/:id
# e. PATCH /powers/:id
class PowerByIdResource(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
        # Serialize only id, name, and description as per requirements
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name
        }
        return make_response(jsonify(power_dict), 200)

    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
        data = request.get_json()
        new_description = data.get('description')

        if not new_description:
            return make_response(jsonify({"errors": ["Description is required for update"]}), 400)

        try:
            # Validate description through the model's @validates decorator
            power.description = new_description
            db.session.commit()
            
            # Return updated power as per requirements
            updated_power_dict = {
                "description": power.description,
                "id": power.id,
                "name": power.name
            }
            return make_response(jsonify(updated_power_dict), 200)
        except ValueError as e:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(e)]}), 400) # Bad Request
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": ["An unexpected error occurred: " + str(e)]}), 500)

api.add_resource(PowerByIdResource, '/powers/<int:id>')

# f. POST /hero_powers
class HeroPowersResource(Resource):
    def post(self):
        data = request.get_json()
        
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        # Check if hero and power exist
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero:
            return make_response(jsonify({"errors": ["Hero not found"]}), 404)
        if not power:
            return make_response(jsonify({"errors": ["Power not found"]}), 404)

        try:
            new_hero_power = HeroPower(
                strength=strength,
                hero_id=hero_id,
                power_id=power_id
            )
            db.session.add(new_hero_power)
            db.session.commit()

            # Construct the response as specified, including nested hero and power details
            response_dict = {
                "id": new_hero_power.id,
                "hero_id": new_hero_power.hero_id,
                "power_id": new_hero_power.power_id,
                "strength": new_hero_power.strength,
                "hero": {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name
                },
                "power": {
                    "description": power.description,
                    "id": power.id,
                    "name": power.name
                }
            }
            return make_response(jsonify(response_dict), 201) # Created
        except ValueError as e:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(e)]}), 400) # Bad Request
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": ["An unexpected error occurred: " + str(e)]}), 500)

api.add_resource(HeroPowersResource, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)