#!/usr/bin/python3
"""Default restful api actions for user"""

from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id=None):
    """Method to retrieve list of all user objects or user object by id"""
    if user_id is None:
        user_list = []
        for obj in storage.all(User).values():
            user_list.append(obj.to_dict())
        return jsonify(user_list)
    for obj in storage.all(User).values():
        if obj.id == user_id:
            user = obj.to_dict()
            return user
    abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_user(user_id):
    """Deletes user object by id"""
    for obj in storage.all(User).values():
        if obj.id == user_id:
            obj.delete()
            storage.save()
            return ({}, 200)
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Method that transforms HTTP body request to a new user"""
    jreq = request.get_json(silent=True)

    if jreq is None:
        abort(400, 'Not a JSON')
    if 'email' not in jreq:
        abort(400, 'Missing email')
    if 'password' not in jreq:
        abort(400, 'Missing password')
    new_user = User(**jreq)
    storage.save()
    return jsonify(new_User.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    """Update user object"""
    for obj in storage.all(User).values():
        if obj.id == user_id:
            user = obj.to_dict()
            jreq = request.get_json(silent=True)
            if jreq is None:
                abort(400, 'Not a JSON')
            for key, value in jreq.items():
                if key == 'id' or key == "created_at" or key == "updated_at" or key == 'email':
                    continue
                setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
