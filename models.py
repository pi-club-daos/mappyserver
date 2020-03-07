import json
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from sqlalchemy.ext.declarative import DeclarativeMeta

# this class represents the data table in the db
class ReadingFile(db.Model):
    __tablename__ = 'DataReadings'

    date = db.Column(db.String, primary_key=True)
    hour = db.Column(db.String, primary_key=True)
    minutes = db.Column(db.String, primary_key=True)
    seconds = db.Column(db.String, primary_key=True)
    district = db.Column(db.String, primary_key=True)
    reading = db.Column(db.Float)

    def __repr__(self):
        return '%s-%s-%s-%s,%s,%f;' % (self.date,self.hour,self.minutes,self.seconds,self.district,self.reading)

# helper class to jsonify a db table row
class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)