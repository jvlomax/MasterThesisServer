from flask import jsonify
from flask.views import MethodView


class BaseView(MethodView):
    def make_response(self, message, status, status_code, payload=None):
        response = {"message": message, "status": status}
        if payload:
            response["payload"] = payload

        return jsonify(response), status_code