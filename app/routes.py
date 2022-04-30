from app import app, db, oauth
from flask import request,render_template, url_for,redirect,session
from app.models import SensorValue
import sys
from app.forms import SelectSensorForm
from app.forms import SelectSiteForm
from auth_decorator import login_required
import json



@app.route('/')
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)



@app.route('/auth')
def auth():
    print("here")
    token = oauth.google.authorize_access_token()
    user = token.get('userinfo')
    if user:
        session['user'] = user
    return redirect(url_for('index'))

@app.route('/index')
@login_required
def index():
    print('here')
    return render_template('index.html')


@app.route('/dam-information/get-all',methods=['GET'])
@login_required
def allSensor():
   
    vals = SensorValue.query.order_by(SensorValue.timestamp.desc()).all()
    print(vals)
    return render_template('sensorData.html', sensorVals = vals)

@app.route('/select-sensor', methods=['GET', 'POST'])
@login_required
def selectSensor():
    form = SelectSensorForm()

    if form.validate_on_submit():
        if SensorValue.query.filter_by(sensor = form.sensor.data).first() is not None:
            return redirect(url_for( 'particularSensor', sensorID = form.sensor.data))

    return render_template('select.html', form = form)

@app.route('/select-site', methods=['GET', 'POST'])
@login_required
def selectSite():
    form = SelectSiteForm()
    
    if form.validate_on_submit():
        if SensorValue.query.filter_by(site = form.site.data).first() is not None:
            return redirect(url_for( 'particularSite', siteID = form.site.data))
           

    return render_template('selectSite.html', form = form)


@app.route('/dam-information/get/<sensorID>',methods=['GET'])
@login_required
def particularSensor(sensorID):
    vals = SensorValue.query.filter_by(sensor = sensorID).all()
    print(vals)
    return render_template('sensorData.html', sensorVals = vals)


@app.route('/dam-information/get/site/<siteID>',methods=['GET'])
@login_required
def particularSite(siteID):

    vals = SensorValue.query.filter_by(site = siteID).all()
    graphVals = {"x":[], "y":[], "type":'scatter'}
    for val in vals:
        
        graphVals["x"].append(val.timestamp.strftime('%m/%d/%Y'))
        graphVals["y"].append(val.flow_rate)

    return render_template('siteData.html', siteVals = vals, graphVals = json.dumps(graphVals))


@app.route('/dam-information/update',methods=['POST'])
@login_required
def addDamData():

    json = request.get_json()

    try:
        sensorVals = SensorValue(sensor = json['sensor'], flow_rate = json['flow_rate'], site = json['site'])
        
        db.session.add(sensorVals)
        db.session.commit()
    except Exception: 
        return Exception, 400

    return 'Data recorded'