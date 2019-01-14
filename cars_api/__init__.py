from flask import Flask
import os

# Constants
APP_DB_URI = f'sqlite:////{os.path.abspath(os.curdir)}/cars.db'

# Creating the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = APP_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# After creating the apps we can load the DB tools and create an SQL connection
import cars_api.dbtools

# Import the ORM (SQLAlchemy Class)
from cars_api.cars import Cars

# Create a connection to the DB (will be replaced with ORM eventually)
db = cars_api.dbtools.sqlite3_connect()

# After we have an SQL connection, we can load the routes
import cars_api.routes
