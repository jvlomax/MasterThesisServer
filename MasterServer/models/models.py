from MasterServer import db


class Beacon(db.Model):
    id = db.Column(db.String(17), primary_key=True)
    team = db.Column(db.Integer, default=-1)
    guardian = db.Column(db.String(255), default=None, nullable=True)
    location = db.Column(db.String(255), nullable=False)


    def __init__(self, mac_address, location):
        self.guardian = None
        self.location = location
        self.id = mac_address
        self.team = None

    def as_dict(self):
        return {"id": self.id, "team": self.team, "guardian": self.guardian, "location": self.location}

    def repr(self):
        return "<Beacon id: {0} Location: {1}>".format(self.id, self.location)

class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    stats = db.Column(db.String(255), nullable=False)
    team = db.Column(db.Integer, nullable=False)
