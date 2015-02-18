from MasterServer import db
import uuid
class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(17), unique=True)
    def __init__(self, mac_address):
        self.id = uuid.uuid4().int
        self.mac_address = mac_address

