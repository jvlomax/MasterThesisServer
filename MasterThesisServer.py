from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

db = SQLAlchemy(app)

class Beacon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.integer, default=0)
    guradian = db.Column(db.Text, default=None, nullable=True)

class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    stats = db.Column(db.Text, nullable=False)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/beacon/info/<integer:id>")
def beacon_info(id):
    beacon = Beacon.get(id)
    return jsonify(beacon)


if __name__ == '__main__':
    app.run()
