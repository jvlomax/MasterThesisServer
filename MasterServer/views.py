from flask import jsonify, render_template, make_response
from MasterServer.utils.exceptions import DatabaseError, MalformedExpression
from MasterServer.models.device import Devices
from MasterServer import app,db

from MasterServer.resources.beacons import BeaconsView
from MasterServer.resources.guardians import GuardiansView


def register_api(view, endpoint, url, pk="id", pk_type="int"):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=["GET",])
    app.add_url_rule(url, view_func=view_func, methods=["POST"])
    app.add_url_rule("{0}<{1}:{2}>".format(url, pk_type, pk), view_func=view_func, methods=["GET", "PUT", "DELETE"])


register_api(BeaconsView, "beacons_view", "/beacons/", pk="id", pk_type="path")
register_api(GuardiansView, "guardians_view", "/guardians/", pk="id", pk_type="int")


@app.route("/register/<path:mac_address>")
def register_device(mac_address):
    device = Devices(mac_address)

    db.session.add(device)
    db.session.commit()

    resp = make_response(jsonify({"status": 200, "message": "Deveice sucessfully register", "uuid": device.id}))
    resp.set_cookie("uuid", device.id, 2592000)

    return resp

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.errorhandler(DatabaseError)
def handle_database_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(MalformedExpression)
def handle_malformed_expression(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

client = app.test_client()
