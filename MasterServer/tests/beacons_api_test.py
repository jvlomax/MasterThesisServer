import unittest
import os
import json
from flask.ext.testing import TestCase

from MasterServer import app, db
from MasterServer.config import TestConfig


class BeaconTestCase(TestCase):
    DEFAULT_ID = "00-00-00-00"
    DEFAULT_LOCATION = "test location"
    DEFAULT_GUARDIAN = None
    MANY = 10
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
        if "test.db" in os.listdir():
            os.unlink("test.db")

    def test_empty_db(self):
        rv = self.client.get("/beacons/{}".format(self.DEFAULT_ID))


        assert rv.status_code == 404

    def test_craete_new(self):
        rv = self.client.post("/beacons/", data={"mac_address": self.DEFAULT_ID,
                                       "location": self.DEFAULT_LOCATION,
                                       "guardian": self.DEFAULT_LOCATION})

        self.assert200(rv)

        rv = self.client.get("/beacons/{}".format(self.DEFAULT_ID))

        self.assert200(rv)

    def test_create_many(self):
        start = self.DEFAULT_ID
        for i in range(0, self.MANY):
            rv = self.client.post("/beacons/", data={"mac_address": start,
                                                     "location": self.DEFAULT_LOCATION,
                                                     "guardian": self.DEFAULT_GUARDIAN})
            self.assert200(rv)
            last_digit = int(start[-1])
            start = start[:-1] + str(last_digit + 1)

    def test_get_many(self):
        self.test_create_many()
        rv = self.client.get("/beacons/")

        self.assert200(rv)
        self.assertEquals(len(rv.json), self.MANY)


    def test_update(self):
        self.test_craete_new()
        new_location = "other test location"
        new_guardian = 5
        new_team = 2
        rv = self.client.put("/beacons/{}".format(self.DEFAULT_ID),
                             data={"team" : new_team,
                                   "location": new_location,
                                   "guardian_id": new_guardian})
        self.assert200(rv)
        rv = self.client.get("/beacons/{}".format(self.DEFAULT_ID))
        self.assert200(rv)

        data = rv.json
        self.assertEquals(data["location"], new_location)
        self.assertEquals(data["guardian"], new_guardian)
        self.assertEquals(data["team"], new_team)

    def test_delete(self):
        self.test_craete_new()
        rv = self.client.get("/beacons/{}".format(self.DEFAULT_ID))
        self.assert200(rv)
        rv = self.client.delete("/beacons/{}".format(self.DEFAULT_ID), data={"secret": "secret"})
        self.assert200(rv)
        rv = self.client.get("/beacons/{}".format(self.DEFAULT_ID))
        self.assert404(rv)



    def test_malformed_mac(self):
        rv = self.client.post("/beacons/", data={"mac_address": "asdefadsajdhasdkasjdsad",
                                       "location": self.DEFAULT_LOCATION,
                                       "guardian": self.DEFAULT_LOCATION})
        self.assert500(rv)
if __name__ == "__main__":
    unittest.main()