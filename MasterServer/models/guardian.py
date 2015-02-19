from MasterServer import db


class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    stats = db.Column(db.String(255), nullable=False)
    team = db.Column(db.Integer, nullable=True)
    owner_id = db.Column(db.Integer, nullable=True)

    def __init__(self, name, stats, team=None, owner_id=None):
        self.name = name
        self.stats = stats
        self.team = team
        self.owner_id = owner_id

    def __repr__(self):
        return "<Guardian id: {0} name: {1} team: {} owner: >".format(self.id, self.location, self.team, self.owner_id)

    def as_dict(self):
        return {"id": self.id, "team": self.team, "name": self.name, "stats": self.stats, "owner_id": self.owner_id}