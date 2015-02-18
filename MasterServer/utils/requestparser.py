from flask import request
import json
from copy import deepcopy
class Argument:

    def __init__(self, name, type, required):

        self.name = name
        self.type = type
        self.required = required

class RequestParser:


    def __init__(self, arguments=None):

        self.arguments = []


    def add_argument(self, name, type, strict=False, required=False, ):
        arg = Argument(name, type, required=required, )
        self.arguments.append(arg)

    def parse_args(self, strict=False):
        data = request.json
        if not data:
            data = json.loads(request.data)
            if not data:
                return None

        # check for required arguments
        for arg in self.argsuments:
            if arg.required and  arg.name not in data:
                return None

        # If strict, make sure no other arguments are included
        if strict:
            for key, value in data:
                if key not in [arg.name for arg in self.arguments]:
                    return None

        return data

    def copy(self):
        parser_copy = RequestParser()
        parser_copy.arguments = deepcopy(self.arguments)
        return parser_copy