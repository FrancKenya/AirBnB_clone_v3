#!/usr/bin/python3
""" manages  the control of Flask """

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import make_response
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """calls storage.close to close connection to the database"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    if not host:
        host = "0.0.0.0"
    port = os.getenv("HBNB_API_PORT")
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
