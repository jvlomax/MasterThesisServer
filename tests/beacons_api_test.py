from flask.ext.testing import TestCase
import unittest
from server import app, db
from config import TestConfig


class BeaconTestCase(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        rv = self.client.get("/beacon/1")

        assert rv.status_code == 404

    def test_craete_new(self):
        rv = self.client.post("/beacon", data={"mac_address": "00-00-00-00",
                                       "location": "test location",
                                       "guardian": None})
        print(rv.data)
        rv = self.client.get("/beacon/1")
        print(rv.data)
        self.assertNotEqual(rv.status_code, 500)

if __name__ == "__main__":
    unittest.main()