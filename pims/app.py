import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from collections import namedtuple
from .model.model import *
from sqlalchemy import desc
from dateutil import parser
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
	handleSetResponseMessage ('add_drug', 'Drug Added successfully!', False)
	emit('listdrugs', dlist, broadcast=True)

@socketio.on('updatedrug')
def handleUpdateDrug(data):
	# print(data['drug']['DrugId'])
	drug = Drug.query.filter(Drug.DrugId == data['drug']['DrugId']).first()
	if drug != None:
		drug.DrugBrandName = data['drug']['DrugBrandName']
		drug.DrugGenericName = data['drug']['DrugGenericName']
		db.session.flush()

		for dose in data['removeDose']:
			dDose = DrugDosage.query.filter(DrugDosage.DrugDosageId == dose['DrugDosageId'], DrugDosage.drug_id == dose['drugId']).first()
			db.session.delete(dDose)
			db.session.flush()
		
		for aDose in data['addDoses']:
			nDose = DrugDosage()
			nDose.DrugDosageDesc = aDose['DrugDosageDesc']
			nDose.drug_id = dose['drugId']
			db.session.add(nDose)
			db.session.flush()
		db.session.commit()

		dlist = handleFetchDrugs()
		handleSetResponseMessage ('update_drug', 'Drug data updated successfully!', False)
		emit('listdrugs', dlist, broadcast=True)
	else:
		handleSetResponseMessage ('update_drug', 'Drug data update failed!', True)

@socketio.on('getAuth')
def handleGetAuth(req):
	u = User.query.filter(User.UserUname == req['uname'], User.UserPassword == base64.b64decode(req['upass'])).first()
	if u == None:
		handleSetResponseMessage ('login', 'Error with User credentials! \nTry Again.', True)
	else:
		usr = UserSchema.dump(u).data
		auth = handleCreateAuth(usr)
		handleSetResponseMessage ('login', 'Login Successful!', False)
		preferences = handleGetPreferences()
		emit('grantAuth', auth)
		emit('acceptPreferences', preferences)

@socketio.on('updatehospital')
def handleUpdateHospital(data):
	h = HospitalSetup.query.first()
	h.HospitalSetupName = data['HospitalName']
	h.HospitalSetupAddress = data['HospitalAddress']
	
	db.session.commit()
	preferences = handleGetPreferences()
	handleSetResponseMessage ('update_hospital', 'Affilliated Hospital updated successfully!', False)
	emit('acceptPreferences', preferences, broadcast=True)

@socketio.on('updatedoctor')
def handleUpdateDoctor(data):
	d = DoctorSetup.query.first()
	d.DoctorSetupName = data['DoctorSetupName']
	d.DoctorSetupMembershipBody = data['DoctorSetupMembershipBody'] 
	d.DoctorSetupLic = data['DoctorSetupLic']
	d.DoctorSetupPtr = data['DoctorSetupPtr']
	d.DoctorSetupS2 = data['DoctorSetupS2']
	d.DoctorSetupMembership = data['DoctorSetupMembership']

	db.session.commit()
	preferences = handleGetPreferences()
	handleSetResponseMessage ('update_doctor', 'Doctor information updated successfully!', False)
	emit('acceptPreferences', preferences, broadcast=True)

@socketio.on('updateclinic')
def handleUpdateClinic(data):
	c = ClinicSetup.query.first()
	c.ClinicSetupName = data['ClinicSetupName'] 
	c.ClinicSetupAddress = data['ClinicSetupAddress']
	obj = json.dumps(data['ClinicSetupSchedule'])
	c.ClinicSetupSchedule = obj

	db.session.commit()
	preferences = handleGetPreferences()
	handleSetResponseMessage ('update_clinic', 'Clinic information updated successfully!', False)
	emit('acceptPreferences', preferences, broadcast=True)

@socketio.on('updatepassword')
def handleUpdatePassword(data):
	u = User.query.filter(User.UserUname == data['Uname'], User.UserPassword == data['CurrentPass']).first()
	if u == None:
		handleSetResponseMessage ('change_password', 'Incorrect current password! \nTry Again.', True)
	else:
		u.UserPassword = data['NewPass']
		db.session.commit()

		handleSetResponseMessage ('change_password', 'Password updated successfully!', False)

@socketio.on('removedrug')
def handleRemoveDrug(data):
	d = Drug.query.filter(Drug.DrugId == data['DrugId']).first()
	d.DrugStatus = "archived"

	db.session.commit()
	dlist = handleFetchDrugs()
	handleSetResponseMessage ('delete_drug', 'Drug deleted successfully!', False)
	emit('listdrugs', dlist, broadcast=True)
	
@socketio.on('getdirections')
def handleGetDirections():
	di = []

	for d in DirectionsSetup.query.all():
		dx = {}
		directions = DirectionsSetupSchema.dump(d)
		dx['value'] =  str(d.DirectionsSetupContent)
		dx['label'] =  str(d.DirectionsSetupContent)
		di.append(dx)

	emit('listdirections', di)

@socketio.on('addpatient')
def handleAddPatient(data):
	p = Patient()
	p.PatientFname = data['PatientFname']
	p.PatientMname = data['PatientMname']
	p.PatientLname = data['PatientLname']
	p.PatientExt = data['PatientExt']
	p.PatientSex = data['PatientSex']
	p.PatientBirthdate = data['PatientBirthdate']
	p.PatientAddress = data['PatientAddress']
	p.PatientContact = data['PatientContact']
	p.PatientReligion = data['PatientReligion']
	db.session.add(p)
	db.session.flush()

	pId = p.PatientId
	pd = PatientDetails()
	pd.patient_id = pId
	pd.PatientDetailsFather =  json.dumps(data['details']['father'])
	pd.PatientDetailsMother =  json.dumps(data['details']['mother'])
	image = base64.b64decode(data['details']['photo'].encode("utf-8"))
	pd.PatientDetailsPhoto = image
	db.session.add(pd)
	db.session.commit()
	# print(p)

#NON WS FUNCTIONS
def handleGetPreferences():
	hospital = HospitalSetupSchema.dump(HospitalSetup.query.first()).data
	clinic = ClinicSetupSchema.dump(ClinicSetup.query.first()).data
	doctor = DoctorSetupSchema.dump(DoctorSetup.query.first()).data
	clinic['ClinicSetupSchedule'] = json.loads(clinic['ClinicSetupSchedule'])
	dump = json.dumps({'clinic': clinic, 'hospital': hospital, 'doctor': doctor})
	strD = base64.b64encode(dump.encode('utf-8'))
	print(clinic)
	return strD

def handleCreateAuth(udata):
	udata['is_authenticated'] = True
	udata.pop('UserPassword', None)
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
		resClass = {'classes': 'red', 'icon': 'fa-solid fa-circle-exclamation text-3xl'}
	else:
		resClass = {'classes': 'green', 'icon': 'fa-solid fa-circle-check text-3xl'}
	
	return resClass

def handleFetchDrugs():
	dlist = []
	for d in Drug.query.filter(Drug.DrugStatus == 'active').order_by(Drug.DrugBrandName).all():
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
