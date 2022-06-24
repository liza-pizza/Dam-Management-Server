from app import db
from datetime import datetime
import enum


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
        
class SensorValue(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    reading = db.Column(db.Integer, db.ForeignKey('site.id'))
    
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    serialNumber = db.Column(db.String(128))
    readings = db.relationship('sensorValue', backref='sensor readings', lazy='dynamic')

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensors_at_location = db.relationship('sensor', backref='sensors at site', lazy='dynamic')
    location = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64), index=True)
    district = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64), index=True)

class ReadingType(enum.Enum):
    WATER_DEPTH = "Water Depth"
    FLOW_RATE = "Flow Rate"


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorsoftype = db.relationship('sensorValue', backref='sensors of a type', lazy='dynamic')
    fruit_type = db.Column(db.Enum(ReadingType))
    
