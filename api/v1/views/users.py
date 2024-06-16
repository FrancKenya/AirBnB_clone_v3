#!/usr/bin/python3
"""
This module handles restful api for users
"""

from api.v1.views import app_views
from flask import *
from models import storage
from models.user import User


@app_views.route("/users/", methods=["GET"], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_users(user_id=None):
    """
    Retrieves all users or a specific user
    """
    if user_id:
        user = storage.get(User, user_id)
        if user:
            return make_response(jsonify(user.to_dict()), 200)
        else:
            abort(404)
    else:
        users = [user.to_dict() for user in storage.all(User).values()]
        return make_response(jsonify(users), 200)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """delete a user in the database"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/users/", methods=["POST"], strict_slashes=False)
def post_user():
    """posts an instance of a user to the users table"""
    if not request.get_json():
        return make_response({"error": "Not a JSON"}, 400)
    elif "email" not in request.get_json():
        return make_response({"error": "Missing email"}, 400)
    elif "password" not in request.get_json():
        return make_response({"error": "Missing password"}, 400)
    else:
        user_name = request.get_json()
        user_obj = User(**user_name)
        user_obj.save()
        return make_response(jsonify(user_obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """updates an instance of a user in the users table"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    elif not request.get_json():
        return make_response({"error": "Not a JSON"}, 400)
    else:
        body = request.get_json()
        for key, value in body.items():
            if key not in ["created_at", "update_at", "id"]:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
