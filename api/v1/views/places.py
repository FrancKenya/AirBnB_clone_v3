#!/usr/bin/python3
"""
This module handles url views interaction with places sql table
"""

from api.v1.views import app_views
from flask import *
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


def list_contains_list(list1, list2):
    """checks if list 1 contains list 2"""
    # Check if items in list 2 are present in 1
    return all(item in list1 for item in list2)


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """returns all places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return make_response(jsonify(places), 200)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """returns a place item"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """deletes a place item"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """creates a place item"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_id = request.get_json().get("user_id")
    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json().get("name"):
        return make_response(jsonify({"error": "Missing name"}), 400)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """updates a place item"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "city_id, user_id"]:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search():
    """searches for places with given params"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    params = request.get_json()
    if not params or params == {}:
        return make_response(jsonify(
            [place.to_dict()for place in storage.all(Place).values()]))
    if params:
        states = params.get('states', None)
        cities = params.get('cities', None)
        amenities = params.get('amenities', None)

        places_list = []
        cities_list = []

        if states and states != []:
            all_states = [storage.get(State, id) for id in states]
            for state in all_states:
                if state:
                    for city in state.cities:
                        cities_list.append(city)
        if cities and cities != []:
            for id in cities:
                city = storage.get(City, id)
                if city and city not in cities_list:
                    cities_list.append(city)
        for city in cities_list:
            for place in city.places:
                places_list.append(place)

        amenities_list = []
        if amenities and amenities != []:
            for id in amenities:
                amenity = storage.get(Amenity, id)
                if amenity:
                    amenities_list.append(amenities)
        if amenities_list and amenities_list != []:
            for place in places_list:
                if not list_contains_list(place.amenities, amenities_list):
                    places_list.remove(place)
        return make_response(
            jsonify([place.to_dict() for place in places_list]))
