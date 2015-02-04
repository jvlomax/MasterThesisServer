from flask import Flask, jsonify, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import DevConfig as config
from flask.ext import restful
app = Flask(__name__)

db = SQLAlchemy(app)
api = restful.Api(app)
app.config.from_object(config)


class DatabaseError(Exception):
    status_code = 500
    def __init__(self, payload=None):
        super().__init__()
        self.payload = payload
        self.message = "Database error"
    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv





from models import *
from beacons_view import Beacons_view


api.add_resource(Beacons_view, "/beacon/<string:id>", "/beacon")


def init_db():
    db.init_app(app)
    db.create_all()

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.errorhandler(DatabaseError)
def handle_database_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    init_db()

    app.run()
