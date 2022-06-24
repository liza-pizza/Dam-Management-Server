from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField,SelectField
from wtforms.validators import DataRequired
from app.models import SensorValue


class SelectSensorForm(FlaskForm): 
    sensor = SelectField('Sensor Number',  render_kw={'style': 'width: 10ch'})
    submit = SubmitField('Submit')


class SelectSiteForm(FlaskForm):
    site = SelectField('Site',render_kw={'style': 'width: 10ch'})
    submit = SubmitField('Submit')

