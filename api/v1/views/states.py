#!/usr/bin/python3
"""
Create class api
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', strict_slashes=False)
def get_states():
	"""Retrieve the list of all State objects: GET /api/v1/states"""
	states = storage.all(State).values()
	states_list = [state.to_dict() for state in states]
	return jsonify(states_list)

@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_id(state_id):
	"""Retrieve a State object: GET /api/v1/states/<state_id>"""
	state = storage.get(State, state_id)
	if state:
		return jsonify(state.to_dict())
	else:
		abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
	"""Delete a State object: DELETE /api/v1/states/<state_id>"""
	state = storage.get(State, state_id)
	if state:
		storage.delete(state)
		storage.save()
		return jsonify({}), 200
	else:
		abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
	"""Create a State: POST /api/v1/states"""
	if not request.is_json:
		return make_response(jsonify({"error": "Not a JSON"}), 400)

	kwargs = request.get_json()
	if 'name' not in kwargs:
		return make_response(jsonify({"error": "Missing name"}), 400)

	state = State(**kwargs)
	state.save()
	return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
	"""Update a State object: PUT /api/v1/states/<state_id>"""
	if not request.is_json:
		return make_response(jsonify({"error": "Not a JSON"}), 400)

	state = storage.get(State, state_id)
	if not state:
		return abort(404)

	data = request.get_json()
	ignore_keys = ['id', 'created_at', 'updated_at']

	for key, value in data.items():
		if key not in ignore_keys:
			setattr(state, key, value)
	state.save()
	return jsonify(state.to_dict()), 200
