from sqlalchemy import true
from app import app, db, oauth
from flask import request,render_template, url_for,redirect,session
from app.models import SensorValue
import sys
from app.forms import SelectSensorForm
from app.forms import SelectSiteForm
from auth_decorator import login_required
from datetime import datetime, timedelta
import json



@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)



@app.route('/auth')
def auth():

    token = oauth.google.authorize_access_token()
    user = token.get('userinfo')
    if user:
        session['user'] = user
    return redirect(url_for('index'))

       
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/dam-information/get-all',methods=['GET'])
def allSensor():
    seven_days_filter = datetime.today() - timedelta(days = 7)
    vals = SensorValue.query.order_by(SensorValue.timestamp.desc()).filter(SensorValue.timestamp >= seven_days_filter).all()
    print(vals)
    return render_template('sensorData.html', sensorVals = vals)

@app.route('/select-sensor', methods=['GET', 'POST'])
def selectSensor():
    form = SelectSensorForm()
    setOfSensors = set([])
    for a in SensorValue.query.all():
        setOfSensors.add(a.sensor) 
   
    form.sensor.choices = [(g) for g in setOfSensors]
    if form.validate_on_submit():
        if SensorValue.query.filter_by(sensor = form.sensor.data).first() is not None:
            return redirect(url_for( 'particularSensor', sensorID = form.sensor.data))

    return render_template('select.html', form = form)

@app.route('/select-site', methods=['GET', 'POST'])
def selectSite():
   
    form = SelectSiteForm()
    setOfSites = set([])
    for a in SensorValue.query.all():
        setOfSites.add(a.site) 
    
    form.site.choices = [(g) for g in setOfSites]

    if form.validate_on_submit():
       
        if SensorValue.query.filter_by(site = form.site.data).first() is not None:
            return redirect(url_for( 'particularSite', siteID = form.site.data))
           

    return render_template('selectSite.html', form = form)


@app.route('/dam-information/get/<sensorID>',methods=['GET'])
def particularSensor(sensorID):
    seven_days_filter = datetime.today() - timedelta(days = 7)
    vals = SensorValue.query.filter_by(sensor = sensorID).filter(SensorValue.timestamp >= seven_days_filter).all()
    print(vals)
    graphVals = {"x":[], "y":[], "type":'scatter'}
    for val in vals:
        graphVals["x"].append(val.timestamp.strftime('%m/%d/%Y, %H:%M:%S'))
        graphVals["y"].append(val.water_depth)
  
    print(graphVals)
    return render_template('sensorData.html', sensorVals = vals, graphVals = json.dumps(graphVals))


@app.route('/dam-information/get/site/<siteID>',methods=['GET', 'POST'])
def particularSite(siteID):
    form = SelectSensorForm()
    setOfSensors = set([])
    for a in SensorValue.query.filter_by(site = siteID):
        setOfSensors.add(a.sensor) 
    
    form.sensor.choices = [(g) for g in setOfSensors]
    if form.is_submitted():
        print(form.sensor.data)
    
    
    seven_days_filter = datetime.today() - timedelta(days = 7)
    graphVals = {"x":[], "y":[], "type":'scatter'}
    vals = []
    if form.is_submitted():
        vals = SensorValue.query.filter_by(site = siteID, sensor = form.sensor.data).filter(SensorValue.timestamp >= seven_days_filter).all()
        
        for val in vals:
            
            graphVals["x"].append(val.timestamp.strftime('%m/%d/%Y, %H:%M:%S'))
            graphVals["y"].append(val.water_depth)
    

    return render_template('siteData.html', siteVals = vals, graphVals = json.dumps(graphVals), form = form)

@app.route('/prediction')
def pred(): 
    return render_template('pred.html')

@app.route('/dam-information/update',methods=['POST'])
def addDamData():

    json = request.get_json()

    try:
        sensorVals = SensorValue(sensor = json['sensor'], water_depth = json['water_depth'], site = json['site'])
        
        db.session.add(sensorVals)
        db.session.commit()
    except Exception: 
        return Exception, 400

    return 'Data recorded'