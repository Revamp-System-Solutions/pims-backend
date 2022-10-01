import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from collections import namedtuple
from .model.model import *
from sqlalchemy import desc
from datetime import date, datetime, timedelta
import dateparser
from .model.schema import *
import base64
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pims:password@localhost/pims'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('connect')
def handleConnect():
	now = datetime.now()
	dow = calendar.day_name[now.weekday()]
	print(dow + " Connected")

@socketio.on('getpatients')
def handleGetPatients(d):
	plist = []
	for p in Patient.query.filter(Patient.PatientFname.like(d)).all():
		pd = PatientDetails.query.filter(PatientDetails.patient_id == p.PatientId).first()
		tmpP = PatientSchema.dump(p).data
		tmpP['patient_details'] = PatientDetailsSchema.dump(pd).data
		bd = tmpP['PatientBirthdate'].split("-")
		tmpP['PatientAge'] = calculateAge(date(int(bd[0]), int(bd[1]), int(bd[2])))
		plist.append(tmpP)

	emit('listpatients', plist)

@socketio.on('getdrugs')
def handleGetDrugs():
		dlist = handleFetchDrugs()
		emit('listdrugs', dlist)

@socketio.on('adddrugs')
def handleAddDrugs(data):
	for d in data:
		drug = Drug()
		drug.DrugBrandName = d['DrugBrandName']
		drug.DrugGenericName = d['DrugGenericName']
		db.session.add(drug)
		db.session.flush()

		drugId = drug.DrugId

		for dd in d['drug_dosage']:
			ddose = DrugDosage()
			ddose.DrugDosageDesc = dd['DrugDosageDesc']
			ddose.drug_id = drugId
			db.session.add(ddose)
			db.session.flush()
		db.session.commit()
	dlist = handleFetchDrugs()
	emit('listdrugs', dlist, broadcast=True)

@socketio.on('getAuth')
def handleGetAuth(req):
	u = User.query.filter(User.UserUname == req['uname'], User.UserPassword == base64.b64decode(req['upass'])).first()
	if u == None:
		handleSetResponseMessage ('login', 'Error with User credentials! \nTry Again.', True)
	else:
		usr = UserSchema.dump(u).data
		auth = handleCreateAuth(usr)
		handleSetResponseMessage ('login', 'Login Successful!', False)
		emit('grantAuth', auth)

#NON WS FUNCTIONS
def handleCreateAuth(udata):
	udata['is_authenticated'] = True
	dump = json.dumps(udata)
	strD = base64.b64encode(dump.encode('utf-8'))
	return strD

def handleSetResponseMessage (action, message, is_error):
	rClass = handleDefineResponseClass(is_error)
	res = {'action': action, 'message': message, 'throwError': is_error, 'classes': rClass['classes'], 'icon': rClass['icon']}
	emit('requestResponse',res)

def handleDefineResponseClass(data):
	resClass = {}
	if data:
		resClass = {'classes': 'bg-red-500/75', 'icon': 'fa-solid fa-circle-exclamation text-3xl'}
	else:
		resClass = {'classes': 'bg-green-500/75', 'icon': 'fa-solid fa-circle-check text-3xl'}
	
	return resClass

def handleFetchDrugs():
	dlist = []
	for d in Drug.query.all():
		item =  DrugSchema.dump(d).data
		itemdose = []
		for dsId in item['drug_dosage']:
			dsg = DrugDosage.query.filter(DrugDosage.DrugDosageId == dsId).first()
			i = DrugDosageSchema.dump(dsg).data
			itemdose.append(i)
		item['drug_dosage'] = itemdose
		dlist.append(item)
	return dlist


def calculateAge(dob):
	today = date.today()
	age = today.year - dob.year -((today.month, today.day) < (dob.month, dob.day))
	return age
