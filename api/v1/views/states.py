#!/usr/bin/python3
"""
Create class api
"""

from models import storage
from models.state import State
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_states():
	"""gets state objs"""
	states = storage.all(State).values()
	states_list = [state.to_dict() for state in States]
	return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_id(state_id):
	"""gets states with their id"""
	state = storage.get(State, state.to_dict())
	if state:
		return jsonify(state.to_dict())
	else:
		return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
	""" deletes state obj using state id"""
	state = storage.get(State, state_id)
	if state:
		storage.delete(state)
		storage.save()
		return jsonify({}), 200
	else:
		abort(404)


@app_views.route('/state/<state_id>', methods=['POST'], strict_slashes=False)
def create_state():
	"""creates a state object"""
	if request.content_type != 'application/json':
		return abort(404, 'Not a JSON')
	if not request.get_json():
		return abort(400, 'Not a JSON')
	kwargs = request.get_json()

	if 'name' not in kwargs:
		abort(400, 'Missing name')

	state = State(**kwargs)
	state.save()
	return jsonify(state.to_dict()), 200


@app_views.route('/state/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
	"""updates the state object"""
	if request.content_type != 'application/json':
		return abort(400, 'Not a json')
	state = storage.get(State, state_id)
	if state:
		if not request.get_json():
			return abort(400, 'Not a JSON')
		data = request.get_json()
		for key, value in data.items():
			if key not in ignore_keys:
				setattr(state, key, value)
		state.save()
		return jsonify(state.to_dict()), 200
	else:
		return abort(404)
