#!/usr/bin/python3

"""
This module handles url interaction with cities sql table
"""

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """gets an instance of an amenity from the amenities table"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        amenities = [amenity.to_dict() for amenity in
                     storage.all(Amenity).values()]
        return make_response(jsonify(amenities), 200)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """removes an instance of an amenity from the amenities table"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/", methods=["POST"], strict_slashes=False)
def post_amenity():
    """posts an instance of an amenity to the amenities table"""
    if not request.get_json():
        return make_response({"error": "Not a JSON"}, 400)
    elif "name" not in request.get_json():
        return make_response({"error": "Missing name"}, 400)
    else:
        amenity = Amenity(**request.get_json())
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ makes an update to the database"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    elif not request.get_json():
        return make_response({"error": "Not a JSON"}, 400)
    else:
        body = request.get_json()
        for key, value in body.items():
            if key not in ["created_at", "update_at", "id"]:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
