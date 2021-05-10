#!/usr/bin/python3
"""Default restful api actions for amenity"""

from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id=None):
    """Method to retrieve list of all amenity objects or amenity object by id"""
    if amenity_id is None:
        amenity_list = []
        for obj in storage.all(Amenity).values():
            amenity_list.append(obj.to_dict())
        return jsonify(amenity_list)
    for obj in storage.all(Amenity).values():
        if obj.id == amenity_id:
            amenity = obj.to_dict()
            return amenity
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenities(amenity_id):
    """Deletes amenity object by id"""
    for obj in storage.all(Amenity).values():
        if obj.id == amenity_id:
            obj.delete()
            storage.save()
            return ({}, 200)
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """Method that transforms HTTP body request to a new amenity"""
    jreq = request.get_json(silent=True)

    if jreq is None:
        abort(400, 'Not a JSON')
    if 'name' not in jreq:
        abort(400, 'Missing name')
    new_amenity = Amenity(**jreq)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def put_amenity(amenity_id):
    """Update amenity object"""
    for obj in storage.all(Amenity).values():
        if obj.id == amenity_id:
            amenity = obj.to_dict()
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
