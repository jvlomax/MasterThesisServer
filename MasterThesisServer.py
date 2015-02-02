from flask import Flask, jsonify, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import DevConfig as config
app = Flask(__name__)

db = SQLAlchemy(app)
app.config.from_object(config)


class Beacon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, default=0)
    guradian = db.Column(db.String(255), default=None, nullable=True)

class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    stats = db.Column(db.String(255), nullable=False)

db.create_all()
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/beacon/info/<int:id>")
def beacon_info(id):
    beacon = Beacon.get(id)
    return jsonify(beacon)


if __name__ == '__main__':
    app.run()
