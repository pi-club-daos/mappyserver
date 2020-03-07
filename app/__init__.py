from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the flask app
app = Flask(__name__)

# setup the db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kjocpeerznitbs:fb4b8868cc4cc984fdbf2a098b556e2bf2e49f37e51dfa549baf020ebb813311@ec2-46-137-177-160.eu-west-1.compute.amazonaws.com:5432/d3qpmsn94ml9bc'

# create the db connection using the flask helper
db = SQLAlchemy(app)

# and off we go
from app import routes
