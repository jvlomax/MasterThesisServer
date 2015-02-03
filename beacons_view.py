from flask.views import View
from flask import jsonify
from models import *
from server import DatabaseError, db, app
from flask.ext import restful
from flask.ext.restful import reqparse
from sqlalchemy import exc

parser = reqparse.RequestParser()
parser.add_argument("guardian", type=int, help="The id of a guardian")
parser.add_argument("location", type=str, help="Human readable location of the beacon")
parser.add_argument("mac_address", type=str, help="Mac address of the node")

class Beacons_view(restful.Resource):

    def post(self):
        args = parser.parse_args()
        mac_address = args.get("mac_address")
        location = args.get("location")

        try:
            beacon = Beacon(mac_address, location)
            db.session.add(beacon)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            raise DatabaseError
        return jsonify({"status": "200",
                        "message": "beacon created",
                        "new_beacon_id": beacon.id})


    def remove_beacon(self, id):
        b = Beacon.query.get(id)
        db.session.delete(b)
        db.session.commit()

    def get(self, id):
        try:
            b = Beacon.query.get(id)
            if not b:
                return {"status": "404", "message": "Not found"}, 404
            return jsonify(b.as_dict())
        except exc.SQLAlchemyError as e:
            raise DatabaseError


    def move_beacon(self, id, location):
        b = Beacon.query.get(id)
        b.location = location
        db.session.add(b)
        db.session.commit()

    def change_guardian(self, guardian_id, id, team):
        beacon = Beacon.query.get(id)
        beacon.guardian = guardian_id
        guardian = Guardian.query.get(guardian_id)
        beacon.team = guardian.team
        db.session.add(beacon)
        db.session.commit()


