#!/usr/bin/python3
"""Default restful api actions for city"""

from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places_in_city(city_id=None):
    """Method to retrieve list of all places matching city_id"""
    for obj in storage.all(City).values():
        if obj.id == city_id:
            place_list = []
            for place in obj.places:
                place_list.append(place.to_dict())
            return jsonify(place_list)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_places(place_id=None):
    """Method to retrieve place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """Deletes place object by id"""
    for obj in storage.all(Place).values():
        if obj.id == place_id:
            obj.delete()
            storage.save()
            return ({}, 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_place(city_id=None):
    """Method that transforms HTTP body request to a new place"""
    jreq = request.get_json(silent=True)
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    if jreq is None:
        abort(400, 'Not a JSON')
    if 'name' not in jreq:
        abort(400, 'Missing name')
    if 'user_id' not in jreq:
        abort(400, 'Missing user_id')
    print(jreq['user_id'])
    user = storage.get(User, jreq['user_id'])
    print(user)
    if user is None:
        abort(404)
    new_place = Place(**jreq)
    new_place.city_id = city_id
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """Update place object"""
    for obj in storage.all(Place).values():
        if obj.id == place_id:
            place = obj.to_dict()
            jreq = request.get_json(silent=True)
            if jreq is None:
                abort(400, 'Not a JSON')
            for key, value in jreq.items():
                if key == 'id' or key == "created_at" or key == "updated_at" \
                   or key == 'user_id' or key == 'city_id':
                    continue
                setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
    abort(404)
