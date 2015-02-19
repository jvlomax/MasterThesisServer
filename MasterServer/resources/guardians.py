from flask.views import MethodView
from MasterServer.models.guardian import Guardian
import json


class GuardiansView(MethodView):

    def get(self, id):
        if not id:
            guardians = Guardian.query.all()
            li = []
            for guard in guardians:
                li.append([guard.as_dict()])

            return json.dumps(li)
        else:
            guardian = Guardian.get(id)
            return json.dumps(guardian.as_dict())

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def parse_args(self):
        pass
