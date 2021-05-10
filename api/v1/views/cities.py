#!/usr/bin/python3
"""Default restful api actions for city"""

from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities_in_state(state_id=None):
    """Method to retrieve list of all cities matching state_id"""
    for obj in storage.all(State).values():
        if obj.id == state_id:
            city_list = []
            for city in obj.cities:
                city_list.append(city.to_dict())
            return city_list
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_cities(city_id=None):
    """Method to retrieve city object by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def del_city(city_id):
    """Deletes city object by id"""
    for obj in storage.all(City).values():
        if obj.id == city_id:
            obj.delete()
            storage.save()
            return ({}, 200)
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id=None):
    """Method that transforms HTTP body request to a new city"""
    jreq = request.get_json(silent=True)
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if jreq is None:
        abort(400, 'Not a JSON')
    if 'name' not in jreq:
        abort(400, 'Missing name')
    new_city = City(**jreq)
    new_city.state_id = state_id
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """Update city object"""
    for obj in storage.all(City).values():
        if obj.id == city_id:
            city = obj.to_dict()
            jreq = request.get_json(silent=True)
            if jreq is None:
                abort(400, 'Not a JSON')
            for key, value in jreq.items():
                if key == 'id' or key == "created_at" or key == "updated_at":
                    continue
                setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
    abort(404)
