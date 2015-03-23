from flask import jsonify, request
from flask.views import MethodView
import json

class BaseView(MethodView):
    def make_response(self, message: str, status: str, status_code: int, payload=None) -> tuple:
        """
        Create a response to send in return after a method has completed
        :param message: The message to send to the user
        :param status: A human readable status code
        :param status_code: Integer representing the HTTP status code
        :param payload: Optional, if any extra information should be sent (eg. the new object created in db
        :return: returns a tuple with the response formatted to json and the status code as int
        """
        response = {"message": message, "status": status}
        if payload:
            response["payload"] = payload

        return jsonify(response), status_code

    def parse_args(self) -> dict:
        """
        Parses all arguments in request body. It will check the json field first, then try the data field
        :return: dict
        """
        if request.json:
            args = request.json
        else:
            data = request.data
            json.loads(data)
        return args