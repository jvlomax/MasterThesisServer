import unittest
import os
import json
from flask.ext.testing import TestCase

from MasterServer import app, db
from MasterServer.config import TestConfig


class BeaconTestCase(TestCase):


    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @classmethod
    def tearDownClass(cls):
        os.unlink("test.db")

    def test_empty_db(self):
        rv = self.client.get("/beacons/00-00-00-00")


        assert rv.status_code == 404

    def test_craete_new(self):
        rv = self.client.post("/beacons/", data={"mac_address": "00-00-00-00",
                                       "location": "test location",
                                       "guardian": None})
        print(rv)
        self.assert200(rv)

        rv = self.client.get("/beacons/00-00-00-00")
        print(rv)
        self.assert200(rv)



    def test_update(self):
        self.test_craete_new()
        new_location = "other test location"
        new_guardian = 5
        new_team = 2
        rv = self.client.put("/beacons/00-00-00-00",
                             data={"team" : new_team,
                                   "location": new_location,
                                   "guardian_id": new_guardian})
        self.assert200(rv)
        rv = self.client.get("/beacons/00-00-00-00")
        self.assert200(rv)
        data = rv.json
        self.assertEquals(data["location"], new_location)
        self.assertEquals(data["guardian"], new_guardian)
        self.assertEquals(data["team"], new_team)

    def test_delete(self):
        self.test_craete_new()
        rv = self.client.get("/beacons/00-00-00-00")
        self.assert200(rv)
        rv = self.client.delete("/beacons/00-00-00-00", data={"secret": "secret"})
        self.assert200(rv)
        rv = self.client.get("/beacons/00-00-00-00")
        self.assert404(rv)

if __name__ == "__main__":
    unittest.main()