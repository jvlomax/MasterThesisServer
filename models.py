from server import db


class Beacon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer, default=-1)
    guardian = db.Column(db.String(255), default=None, nullable=True)
    location = db.Column(db.String(255), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False)

    def __init__(self, mac_address, location):
        self.guardian = None
        self.location = location
        self.mac_address = mac_address
        self.team = None

    def as_dict(self):
        return {"id": self.id, "team": self.team, "guardian": self.guardian, "location": self.location, "mac_address": self.mac_address}
    def repr(self):
        return "<Beacon id: {0} Location: {1} mac address: {2}>".format(self.id, self.location, self.mac_address)

class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    stats = db.Column(db.String(255), nullable=False)
    team = db.Column(db.Integer, nullable=False)
