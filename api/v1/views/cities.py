#!/usr/bin/python3

"""
This module handles url views interaction with cities sql table
"""

from api.v1.views import app_views
from flask import *
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_state_city(state_id):
    """retrieve all cities from a state"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    cities = [city.to_dict() for city in state_obj.cities]
    return make_response(jsonify(cities), 200)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """retrieve a city from the city table"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete a city from the city table"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """create a city object in the cities table"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif not request.get_json().get("name"):
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        city = City(**request.get_json())
        city.state_id = state.id
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update a city object in the cities table"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        for key, value in request.get_json().items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
