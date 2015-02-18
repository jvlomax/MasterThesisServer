from flask.views import View
from flask import jsonify
from models import *
from server import DatabaseError, db, app
from flask.ext import restful
from flask.ext.restful import reqparse
from sqlalchemy import exc

parser = reqparse.RequestParser()
parser.add_argument("beacon_id", type=int, help="The id of the beacon")
parser.add_argument("guardian_id", type=int, help="The id of a guardian")
parser.add_argument("location", type=str, help="Human readable location of the beacon")
parser.add_argument("mac_address", type=str, help="Mac address of the node")
parser.add_argument("team", type=int, help="The team controlling the beacon")





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

    def put(self):
        args = parser.parse_args()
        print(args)
        id = args.get("beacon_id")

        beacon = Beacon.query.get(id)

        print(args.get("mac_address"))

        beacon.mac_address = args.get("mac_address")

        beacon.location = args.get("location")
        beacon.team = args.get("team")
        beacon.guardian = args.get("guardian_id")



        return jsonify({"status": "200",
                        "message": "beacon moved",
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





