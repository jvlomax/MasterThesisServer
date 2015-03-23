class DatabaseError(Exception):
    """Excetion for all general database erros
    
    .. note::
        Something something
    """
    status_code = 500
    def __init__(self, message="", payload=None):
        super().__init__()
        self.payload = payload
        self.message = str(message)

    def to_dict(self):
        #rv = dict(self.payload or ())
        rv = {}
        rv["message"] = self.message
        rv["status"] = self.status_code
        return rv


class MalformedExpression(Exception):
    status_code = 500
    def __init__(self, message=""):
        super().__init__()
        self.message = str(message)

    def to_dict(self):
        rv = {}
        rv["message"] = self.message
        rv["status"] = self.status_code
        return rv