from .baseView import BaseView
from flask import jsonify, request
from flask.ext.restful import reqparse
from sqlalchemy import exc
from MasterServer.models.beacon import Beacon
from MasterServer import db
from MasterServer.utils.exceptions import DatabaseError, MalformedExpression
import json
import re
parser = reqparse.RequestParser()
parser.add_argument("guardian_id", type=int, help="The id of a guardian")
parser.add_argument("location", type=str, help="Human readable location of the beacon")
parser.add_argument("mac_address", type=str, help="Mac address of the beacon")
parser.add_argument("team", type=int, help="The team controlling the beacon")

#TODO: write new parser or figure another way. "secret" is supposed to be a required argument
delete_parser = parser.copy()
delete_parser.add_argument("device_id", type=int, help="device_id")


class BeaconsView(BaseView):

    def get(self, id):
        print(request.headers.get("uuid"))
        try:
            if not id:
                all = Beacon.query.all()
                l = []
                for item in all:
                    l.append([item.as_dict()])

                return json.dumps(l)
            b = Beacon.query.get(id)
            if not b:
                return self.make_response("Not found", "Not Found", 404)


            return jsonify(b.as_dict())


        except exc.SQLAlchemyError as e:
            print("exception", e)
            raise DatabaseError(message=e)


    def post(self):
        args = parser.parse_args()
        mac_address = args.get("mac_address")
        location = args.get("location")
        if not self.validate_mac_address(mac_address):
            raise MalformedExpression("please check you mac address")
        try:
            beacon = Beacon(mac_address, location)
            db.session.add(beacon)
            db.session.commit()
        except exc.SQLAlchemyError as e:

            raise DatabaseError(e)
        return jsonify({"status": "200",
                        "message": "beacon created",
                        "new_beacon_id": beacon.id}), 200

    def put(self, id):
        args = parser.parse_args()

        beacon = Beacon.query.get(id)
        beacon.location = args.get("location")
        beacon.team = args.get("team")
        beacon.guardian = args.get("guardian_id")
        return jsonify({"status": "200",
                        "message": "beacon moved",
                        "new_beacon_id": beacon.id})


    def delete(self, id):

        print(request.data)
        b = Beacon.query.get(id)
        db.session.delete(b)
        db.session.commit()
        return self.make_response("Beacon {} successfully deleted".format(id), "ok", 200)


    def validate_mac_address(self, mac_address):

        if re.search("^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$", mac_address):
            return True
        else:
            return False
