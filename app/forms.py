from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired
from app.models import SensorValue


class SelectSensorForm(FlaskForm): 
    sensor = IntegerField('Sensor Number')
    submit = SubmitField('Submit')
