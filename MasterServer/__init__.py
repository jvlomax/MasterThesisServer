from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from MasterServer.config import DevConfig as config
app = Flask(__name__)

db = SQLAlchemy(app)
app.config.from_object(config)


import MasterServer.views