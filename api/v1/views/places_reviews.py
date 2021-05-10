#!/usr/bin/python3
"""Default restful api actions for review"""

from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.state import State


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews_in_place(place_id=None):
    """Method to retrieve list of all reviews matching place_id"""
    for obj in storage.all(Place).values():
        if obj.id == place_id:
            review_list = []
            for review in obj.review:
                review_list.append(review.to_dict())
            return jsonify(place_list)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id=None):
    """Method to retrieve review object by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_review(review_id):
    """Deletes review object by id"""
    for obj in storage.all(Review).values():
        if obj.id == review_id:
            obj.delete()
            storage.save()
            return ({}, 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_review(place_id=None):
    """Method that transforms HTTP body request to a new review"""
    jreq = request.get_json(silent=True)
    place = storage.get(place, place_id)

    if place is None:
        abort(404)
    if jreq is None:
        abort(400, 'Not a JSON')
    if 'text' not in jreq:
        abort(400, 'Missing text')
    if 'user_id' not in jreq:
        abort(400, 'Missing user_id')
    user = storage.get(User, jreq['user_id'])
    if user is None:
        abort(404)
    new_review = Review(**jreq)
    new_review.place_id = place_id
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id):
    """Update review object"""
    for obj in storage.all(Review).values():
        if obj.id == review_id:
            review = obj.to_dict()
            jreq = request.get_json(silent=True)
            if jreq is None:
                abort(400, 'Not a JSON')
            for key, value in jreq.items():
                if key == 'id' or key == "created_at" or key == "updated_at" \
                   or key == 'user_id' or key == 'place_id':
                    continue
                setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
    abort(404)
