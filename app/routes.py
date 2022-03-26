from app import app, db
from flask import request,render_template, url_for,redirect
from app.models import SensorValue
import sys
from app.forms import SelectSensorForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dam-information/get-all',methods=['GET'])
def allSensor():
   
    vals = SensorValue.query.order_by(SensorValue.timestamp.desc()).all()
    print(vals)
    return render_template('sensorData.html', sensorVals = vals)

@app.route('/select-sensor', methods=['GET', 'POST'])
def selectSensor():
    form = SelectSensorForm()

    if form.validate_on_submit():
        if SensorValue.query.filter_by(sensor = form.sensor.data).first() is not None:
            return redirect(url_for( 'particularSensor', sensorID = form.sensor.data))

    return render_template('select.html', form = form)


@app.route('/dam-information/get/<sensorID>',methods=['GET'])
def particularSensor(sensorID):
    vals = SensorValue.query.filter_by(sensor = sensorID).all()
    print(vals)
    return render_template('sensorData.html', sensorVals = vals)


@app.route('/dam-information/update',methods=['POST'])
def addDamData():

    json = request.get_json()

    try:
        sensorVals = SensorValue(sensor = json['sensor'], flow_rate = json['flow_rate'])
        db.session.add(sensorVals)
        db.session.commit()
    except Exception: 
        return Exception, 400

    return 'Data recorded'