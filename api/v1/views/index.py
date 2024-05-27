#!/usr/bin/python3
"""Script to handle api response"""

from flask import jsonify
from flask import Flask
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({
        "status": "OK"
        })


@app_views.route('/stats', strict_slashes=False)
def show_stats():
    """
    func to give count
    """
    stats = {
        'users': storage.count('User'),
        'amenities': storage.count('Amenity'),
        'places': storage.count('Place'),
        'review': storage.count('Review'),
        'cities': storage.count('City'),
        'states': storage.count('State'),
        }

    return jsonify(stats)
