#!/usr/bin/python3
"""
Create the flask app
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error(error):
    """Returns error msg"""
    response = {"error": "Not found"}
    return jsonify(response), 404

if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
