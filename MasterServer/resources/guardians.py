from MasterServer.resources.baseView import BaseView
from MasterServer.models.guardian import Guardian
from MasterServer.utils.exceptions import DatabaseError
import json
from MasterServer import db
from sqlalchemy import exc

class GuardiansView(BaseView):

    def get(self, id):
        """

        :param id:
        :return:
        """
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
        args = self.parse_args()
        guardian = Guardian(args.get("name"), args.get("stats"), args.get("team"), args.get("owner"))

        try:
            db.session.add(guardian)
            db.session.commit()
        except Exception:
            raise DatabaseError(message="Could not create guardian")

        return self.make_response("Guardian successfully created with id {}".format(guardian.id), "201", 201)


    def put(self, id):
        args = self.parse_args()
        try:
            guardian = Guardian.get(id)
        except exc.SQLAlchemyError as e:
            raise DatabaseError(message=e)

        guardian.name = args.get("name")
        guardian.team = args.get("team")
        guardian.stats = args.get("stats")
        guardian.owner_id = args.get("owner")

        try:
            db.session.add(guardian)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            raise DatabaseError(message=e)

        self.make_response("Successfully updated info", "success", 200)


    def delete(self, id):
        try:
            guardian = Guardian.get(id)
        except exc.SQLAlchemyError as e:
            raise DatabaseError(message=e)


        db.session.delete(guardian)
        db.session.commit()
        self.make_response("Successfully deleted guardian {}", "Success", 200)