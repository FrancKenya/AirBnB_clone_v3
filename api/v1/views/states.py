#!/usr/bin/python3
"""
This module handles restful api for state
"""

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states(state_id=None):
    """
    Retrieves all states or a specific state
    """
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
    else:
        states = [state.to_dict() for state in storage.all(State).values()]
        return make_response(jsonify(states), 200)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """delete a state in the database"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def post_state():
    """posts an instance of a state to the states table"""
    if not request.get_json():
        return make_response({"error": "Not a JSON"}, 400)
    elif "name" not in request.get_json():
        return make_response({"error": "Missing name"}, 400)
    else:
        state_name = request.get_json()
        state_obj = State(**state_name)
        state_obj.save()
        return make_response(jsonify(state_obj.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """updates an instance of a state in the states table"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not request.get_json():
        return make_response({"error": "Not a JSON"}, 400)
    else:
        body = request.get_json()
        for key, value in body.items():
            if key not in ["created_at", "update_at", "id"]:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
