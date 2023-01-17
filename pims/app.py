import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from collections import namedtuple
from .model.model import *
from sqlalchemy import text, desc, or_, and_
from sqlalchemy.exc import IntegrityError
from dateutil import parser
from datetime import date, datetime, timedelta
import dateparser
from .model.schema import *
import base64
import calendar
import warnings


# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password@localhost/pims'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/pims'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*')

todayServer = datetime.now()
currentYear = todayServer.strftime("%Y")
currentMonth = todayServer.strftime("%m")
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
strMonths = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

@socketio.on('newbase')
def handleNewBase(data):
	# print(data[0])
	for nb in data:
		print(nb['id'])
		pd = PatientDetails.query.filter(PatientDetails.patient_id == nb['id']).first()
		tmp = nb['b64']
		pd.PatientDetailsPhoto = tmp.encode('utf-8')
		# pd.PatientDetailsPhoto = nb['b64']

		#db.session.commit()

@socketio.on('connect')
def handleConnect():
	now = datetime.now()
	dow = calendar.day_name[now.weekday()]
	today = date.today()
	yesterday = today - timedelta(days = 1)
	print(yesterday.strftime("%Y-%d-%m"))
	print(now.strftime("%Y-%d-%m") + " Connected")
	print(currentYear + " Connected")

@socketio.on('getpatients')
def handleGetPatients(d):
	plist = []
	now = datetime.now()
	# print( + " Connected")
	for p in Patient.query.filter(or_(Patient.PatientFname.like(d),Patient.PatientLname.like(d))).all():
		pd = PatientDetails.query.filter(PatientDetails.patient_id == p.PatientId).first()
		tmpP = PatientSchema.dump(p).data
	
		tmpP['patient_details'] = PatientDetailsSchema.dump(pd).data
		bd = tmpP['PatientBirthdate'].split("-")
		tmpP['PatientAge'] = calculateAge(date(int(bd[0]), int(bd[1]), int(bd[2])))
		if len(tmpP['clinic_visit']) != 0:
			for obj in tmpP['clinic_visit']:
				cv = ClinicVisit.query.filter(and_(ClinicVisit.ClinicVisitId == obj, ClinicVisit.ClinicVisitDate == now.strftime("%Y-%m-%d") )).order_by(ClinicVisit.time_created).first()
				
				if cv != None:
					cv = ClinicVisitSchema.dump(cv).data	
					vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == cv['visitDetailsId']).first()
					v = ClinicVisitDetailsSchema.dump(vd).data
					if v['ClinicVisitDetailsStatus'] == "queueing" or v['ClinicVisitDetailsStatus'] == "ok":
						tmpP['clinic_visit'] = cv
						tmpP['clinic_visit']['visit_details'] =v
						reqs = []
						for d in tmpP['clinic_visit']['lab_request']:
							
							req = LabRequest.query.filter(LabRequest.LabRequestId == d).first()
							r = LabRequestSchema.dump(req).data
							lr = LabTypes.query.filter(LabTypes.LabTypesId == r["labTypesId"]).first()
							d = LabTypesSchema.dump(lr).data
							r['name'] = d['LabTypesName']
							reqs.append(r)
						tmpP['clinic_visit']['lab_request'] = reqs
						
					else:
						tmpP['clinic_visit'] = None

				else:
					
					tmpP['clinic_visit'] = None
			tmpP['patient_history']  = handleGetHistories(tmpP['PatientId'])
		else:
			tmpP['clinic_visit'] = None
		plist.append(tmpP)
	
	emit('listpatients', plist)

@socketio.on('addpatient')
def handleAddPatient(data):
	try:
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
		father =json.dumps(data['details']['father'])
		pd.PatientDetailsFather =  father
		mother = json.dumps(data['details']['mother'])
		pd.PatientDetailsMother =  mother
		tmp = data['details']['photo']
		pd.PatientDetailsPhoto = tmp.encode('utf-8')
		db.session.add(pd)
		db.session.commit()
		handleSetResponseMessage ('create_patient', 'Patient Added successfully!', False)
	except:
		handleSetResponseMessage ('create_patient', 'Patient Add failed !', True)

@socketio.on('editpatient')
def handleEditPatient(data):
	try:
		p = Patient.query.filter(Patient.PatientId == data['PatientId']).first()
		p.PatientFname = data['PatientFname']
		p.PatientMname = data['PatientMname']
		p.PatientLname = data['PatientLname']
		p.PatientExt = data['PatientExt']
		p.PatientSex = data['PatientSex']
		p.PatientBirthdate = data['PatientBirthdate']
		p.PatientAddress = data['PatientAddress']
		p.PatientContact = data['PatientContact']
		p.PatientReligion = data['PatientReligion']
		

		pId = p.PatientId
		pd = PatientDetails.query.filter(PatientDetails.PatientDetailsId == data['details']['PatientDetailsId']).first()
		pd.patient_id = pId
		father =json.dumps(data['details']['father'])
		pd.PatientDetailsFather =  father
		mother = json.dumps(data['details']['mother'])
		pd.PatientDetailsMother =  mother
		tmp = data['details']['photo']
		pd.PatientDetailsPhoto = tmp.encode('utf-8')
		db.session.add(pd)
		db.session.commit()
		handleSetResponseMessage ('edit_patient', 'Patient Info updated!', False)
	except:
		handleSetResponseMessage ('edit_patient', 'Patient Add failed !', True)

@socketio.on('archivepatient')
def handleArchivePatient(data):
	try:
		p = Patient.query.filter(Patient.PatientId == data['PatientId']).first()
		pArchive = ArchivePatient()
		pArchive.PatientId = p.PatientId
		pArchive.PatientFname = p.PatientFname
		pArchive.PatientMname = p.PatientMname
		pArchive.PatientLname = p.PatientLname
		pArchive.PatientExt = p.PatientExt
		pArchive.PatientSex = p.PatientSex
		pArchive.PatientBirthdate = p.PatientBirthdate 
		pArchive.PatientAddress = p.PatientAddress
		pArchive.PatientContact = p.PatientContact
		pArchive.PatientReligion = p.PatientReligion
		db.session.add(pArchive)
		pdId = pArchive.PatientId 
		pd = PatientDetails.query.filter(PatientDetails.PatientDetailsId == data['patient_details']['PatientDetailsId']).first()
		pdArchive = ArchivePatientDetails()
		pdArchive.PatientDetailsId = pd.PatientDetailsId
		pdArchive.archive_patient_id = pdId
		pdArchive.patientId = pd.patientId
		pdArchive.PatientDetailsFather = pd.PatientDetailsFather 
		pdArchive.PatientDetailsMother = pd.PatientDetailsMother
		pdArchive.PatientDetailsPhoto = pd.PatientDetailsPhoto 

		db.session.add(pdArchive)

		db.session.delete(p)
		db.session.delete(pd)

		db.session.commit()
		handleSetResponseMessage ('archive_patient', 'Patient Data Archived!', False)
	except:
		handleSetResponseMessage ('archive_patient', 'Failed to Archive Patient Data!', True)

@socketio.on('cancelappointment')
def handleCancelAppointment(data):
	try:
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == data).first()
		vd.ClinicVisitDetailsStatus = "cancelled"
		db.session.commit()
		handleSetResponseMessage ('cancel_appointments', 'Appointment cancelled!', False)
		handleGetTodaysAppointments()
	except:
		handleSetResponseMessage ('cancel_appointments', 'Failed to cancel Appointment!', True)

@socketio.on('tagappointment')
def handleTagAppointment(data):
	try:
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == data).first()
		vd.ClinicVisitDetailsStatus = "no_show"
		db.session.commit()
		handleSetResponseMessage ('tag_appointments', 'Appointment Tagged!', False)
		handleGetTodaysAppointments()
	except:
		handleSetResponseMessage ('tag_appointments', 'Failed to tag Appointment!', True)

@socketio.on('gettodaysappointments')
def handleGetTodaysAppointments():
	try:
		alist = []
		now = datetime.now()
		for v in ClinicVisit.query.filter(ClinicVisit.ClinicVisitDate == now.strftime("%Y-%m-%d")).order_by(ClinicVisit.time_created).all():
			cv = ClinicVisitSchema.dump(v).data	
			cv['ClinicVisitPhysicalExam'] = json.loads(cv['ClinicVisitPhysicalExam'])
			vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == cv['visitDetailsId']).first()
			v = ClinicVisitDetailsSchema.dump(vd).data

			if v['ClinicVisitDetailsStatus'] == "queueing":
				p = Patient.query.filter(Patient.PatientId == cv['patientId']).first()
				pd = PatientDetails.query.filter(PatientDetails.patient_id == cv['patientId']).first()

				tmpP = PatientSchema.dump(p).data
				tmpP['patient_details'] = PatientDetailsSchema.dump(pd).data
				tmpP['patient_details']['PatientDetailsPhoto'] = "data:image/jpeg;base64," + tmpP['patient_details']['PatientDetailsPhoto']
				bd = tmpP['PatientBirthdate'].split("-")
				tmpP['PatientAge'] = calculateAge(date(int(bd[0]), int(bd[1]), int(bd[2])))
				tmpP['clinic_visit'] = cv
				tmpP['clinic_visit']['visit_details'] = v
				reqs = []
				for d in tmpP['clinic_visit']['lab_request']:
					
					req = LabRequest.query.filter(LabRequest.LabRequestId == d).first()
					r = LabRequestSchema.dump(req).data
					lr = LabTypes.query.filter(LabTypes.LabTypesId == r["labTypesId"]).first()
					d = LabTypesSchema.dump(lr).data
					r['name'] = d['LabTypesName']
					reqs.append(r)
				tmpP['clinic_visit']['lab_request'] = reqs
			
				alist.append(tmpP)
		if len(alist) == 0:
			alist = None
		emit('appointmentlist', alist)

	except:
		handleSetResponseMessage ('get_appointments', 'Failed to fetch appointments!', True)

@socketio.on('createappointment')
def handleCreateAppointment(data):
	try:
		try:
			vd = ClinicVisitDetails()
			vd.ClinicVisitDetailsPurpose = data['Purpose']
			db.session.add(vd)
			db.session.flush()

			vdId = vd.ClinicVisitDetailsId
		except:
			handleSetResponseMessage ('create_appointment', 'Appointment Set Failed!', True)

		cv = ClinicVisit()
		cv.ClinicVisitDate =  dateparser.parse(data['VisitDate'])
		cv.ClinicVisitComplaints = data['Complaints']
		cv.ClinicVisitHasAppointment = data['HasAppointment']
		cv.visit_details_id = vdId
		cv.patient_id = data['PatientId']

		db.session.add(cv)
		db.session.commit()
		
		v = ClinicVisitDetailsSchema.dump(vd).data
		val = ClinicVisitSchema.dump(cv).data	
		val['visit_details'] = v
		handleGetTodaysAppointments()
		handleSetResponseMessage ('create_appointment', 'Appointment Successfully Set!', False)
		emit('echophysexam', val)

	except:
		handleSetResponseMessage ('create_appointment', 'Appointment Set Failed!', True)

@socketio.on('docupdateappointment')
def handleDocUpdateAppointment(data):
	try:
		cv = ClinicVisit.query.filter(ClinicVisit.ClinicVisitId == data['cID']).first()
		cv.ClinicVisitComplaints = data['Complaints']
		val = ClinicVisitSchema.dump(cv).data
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == val['visitDetailsId']).first()
		vd.ClinicVisitDetailsPurpose = data['Purpose']
		vd.ClinicVisitDetailsDiagnosis = data['Diagnosis']
		vd.ClinicVisitDetailsPlan = data['Fuplan']
		vd.ClinicVisitDetailsCharge = data['Charge']
		vd.ClinicVisitDetailsStatus = "ok"
		db.session.commit()
	
		v = ClinicVisitDetailsSchema.dump(vd).data	
		val['visit_details'] = v
		
		handleSetResponseMessage ('update_appointment', 'Appointment Updated Successfully!', False)
		emit('echophysexam', val)
		
	except:
		handleSetResponseMessage ('update_appointment', 'Appointment Update Failed!', True)


@socketio.on('savepe')
def handleSavePE(obj):
	try:
		cv = ClinicVisit.query.filter(ClinicVisit.ClinicVisitId == obj['cID']).first()
		cv.ClinicVisitPhysicalExam = json.dumps(obj['data'])
		db.session.commit()
		val = ClinicVisitSchema.dump(cv).data
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == val['visitDetailsId']).first()
		v = ClinicVisitDetailsSchema.dump(vd).data	
		val['visit_details'] = v
		handleSetResponseMessage ('save_visit_pe', 'PE Data Saved Successfully!', False)
		
			
		emit('echophysexam', val)
	except:
		handleSetResponseMessage ('save_visit_pe', 'PE Data Save Failed!', True)
@socketio.on('savenote')
def handleSaveNote(obj):
	
	try:
		cv = ClinicVisit.query.filter(ClinicVisit.ClinicVisitId == obj['cId']).first()
		
		val = ClinicVisitSchema.dump(cv).data
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == val['visitDetailsId']).first()
		vd.ClinicVisitDetailsNotes = obj['data']
		db.session.commit()
		v = ClinicVisitDetailsSchema.dump(vd).data	
		val['visit_details'] = v
		reqs = []
		for d in val['lab_request']:
					
			req = LabRequest.query.filter(LabRequest.LabRequestId == d).first()
			r = LabRequestSchema.dump(req).data
			lr = LabTypes.query.filter(LabTypes.LabTypesId == r["labTypesId"]).first()
			d = LabTypesSchema.dump(lr).data
			r['name'] = d['LabTypesName']
			reqs.append(r)
		val['lab_request'] = reqs
		handleSetResponseMessage ('save_visit_pe', 'Notes Saved Successfully!', False)
		
			
		emit('echophysexam', val)
	except:
		handleSetResponseMessage ('save_visit_pe', 'Notes Save Failed!', True)
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
			nDose.drug_id = drug.DrugId
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
	try:
		h = HospitalSetup.query.first()
		h.HospitalSetupName = data['HospitalName']
		h.HospitalSetupAddress = data['HospitalAddress']
	
		db.session.commit()
		preferences = handleGetPreferences()
		handleSetResponseMessage ('update_hospital', 'Affilliated Hospital updated successfully!', False)
		emit('acceptPreferences', preferences, broadcast=True)
	except:
		handleSetResponseMessage ('update_hospital', 'Affilliated Hospital update failed!', True)
		
@socketio.on('updatedoctor')
def handleUpdateDoctor(data):
	try:
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
	except:
		handleSetResponseMessage ('update_doctor', 'Doctor information update failed!', True)
		
@socketio.on('updateclinic')
def handleUpdateClinic(data):
	try:
		c = ClinicSetup.query.first()
		c.ClinicSetupName = data['ClinicSetupName'] 
		c.ClinicSetupAddress = data['ClinicSetupAddress']
		obj = json.dumps(data['ClinicSetupSchedule'])
		c.ClinicSetupSchedule = obj

		db.session.commit()
		preferences = handleGetPreferences()
		handleSetResponseMessage ('update_clinic', 'Clinic information updated successfully!', False)
		emit('acceptPreferences', preferences, broadcast=True)
	except:
		handleSetResponseMessage ('update_clinic', 'Clinic information update failed!', True)

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
	try:
		d = Drug.query.filter(Drug.DrugId == data['DrugId']).first()
		d.DrugStatus = "archived"

		db.session.commit()
		dlist = handleFetchDrugs()
		handleSetResponseMessage ('delete_drug', 'Drug deleted successfully!', False)
		emit('listdrugs', dlist, broadcast=True)
	except:
		handleSetResponseMessage ('delete_drug', 'Drug deletion failed!', True)
	
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


@socketio.on('savehistories')
def handleSaveHistories(data):

	ph = PatientHistory()
	ph.patient_id = data['pId']
	ph.PatientHistoryResult = data['personal']
	ph.history_type_id = 1
	db.session.add(ph)
	db.session.flush()

	ph1 = PatientHistory()
	ph1.patient_id = data['pId']
	ph1.PatientHistoryResult = data['prenatal']
	ph1.history_type_id = 2
	db.session.add(ph1)
	db.session.flush()

	ph3 = PatientHistory()
	ph3.patient_id = data['pId']
	ph3.PatientHistoryResult = data['vax']
	ph3.history_type_id = 3
	db.session.add(ph3)
	db.session.flush()

	ph4 = PatientHistory()
	ph4.patient_id = data['pId']
	ph4.PatientHistoryResult = data['pvax']
	ph4.history_type_id = 4
	db.session.add(ph4)
	db.session.commit()
	phs = handleGetHistories(data['pId'])

	emit('gethistories', phs)

def handleGetHistories(pId):
	phs = []
	for ph in PatientHistory.query.filter(PatientHistory.patient_id == pId).all():
		phh = PatientHistorySchema.dump(ph).data
		phs.append(phs)
	
	return phs

@socketio.on('updatehistories')
def handleUpdateHistories(data):



	ph = PatientHistory.query.filter(and_(PatientHistory.patient_id == data['pId'], PatientHistory.history_type_id == 1 )).first()
	
	phd = PatientHistorySchema.dump(ph).data
	if phd['PatientHistoryResult'] != data['personal']:
		ph.PatientHistoryResult = data['personal']

	ph1 = PatientHistory.query.filter(and_(PatientHistory.patient_id == data['pId'], PatientHistory.history_type_id == 2 )).first()
	ph1d = PatientHistorySchema.dump(ph1).data
	if ph1d['PatientHistoryResult'] != data['prenatal']:
		ph1.PatientHistoryResult = data['prenatal']


	ph3 = PatientHistory.query.filter(and_(PatientHistory.patient_id == data['pId'], PatientHistory.history_type_id == 3 )).first()
	ph3d = PatientHistorySchema.dump(ph3).data
	if ph3d['PatientHistoryResult'] != data['vax']:
		ph3.PatientHistoryResult = data['vax']
	

	ph4 = PatientHistory.query.filter(and_(PatientHistory.patient_id == data['pId'], PatientHistory.history_type_id == 4 )).first()
	ph4d = PatientHistorySchema.dump(ph4).data
	if ph4d['PatientHistoryResult'] != data['pvax']:
		ph4.PatientHistoryResult = data['pvax']

	db.session.commit()

	phs = handleGetHistories(data['pId'])

	emit('gethistories', phs)
	

@socketio.on('savelab')
def handleSaveLab(data):
	try:
		reqs = []
		for d in data['data']:
			req = LabRequest()
			req.lab_types_id = d['id']
			req.LabRequestBy = data['by']
			req.clinic_visit_id = data['pId']
			db.session.add(req)
			db.session.commit()

			reqs.append(LabRequestSchema.dump(req).data)

		cv = ClinicVisit.query.filter(ClinicVisit.ClinicVisitId == data['pId']).first()
		
		val = ClinicVisitSchema.dump(cv).data
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == val['visitDetailsId']).first()
		v = ClinicVisitDetailsSchema.dump(vd).data	
		val['visit_details'] = v
		val['lab_request'] = reqs
		reqs = []
		for d in val['lab_request']:
					
			req = LabRequest.query.filter(LabRequest.LabRequestId == d).first()
			r = LabRequestSchema.dump(req).data
			lr = LabTypes.query.filter(LabTypes.LabTypesId == r["labTypesId"]).first()
			d = LabTypesSchema.dump(lr).data
			r['name'] = d['LabTypesName']
			reqs.append(r)
		val['lab_request'] = reqs
		handleSetResponseMessage ('save_visit_lab', 'Lab Requests Saved Successfully!', False)
		
			
		emit('echophysexam', val)

	except:	
		handleSetResponseMessage ('save_visit_lab', 'Failed to Save Lab Requests!', True)


@socketio.on('saveprescription')
def handleSavePrescription(objd):
	try:
		pr = Prescription()
		pr.patient_id = objd['pId']
		pr.prescription_type_id = 2 if objd['type'] == 'sprescription' else 1
		db.session.add(pr)
		db.session.flush()
		prId = pr.PrescriptionId
		for pd in objd['data']:
			prD = PrescriptionDetails()
			prD.drug_id = pd['Drug']
			prD.dosage_id = pd['Dosage']
			prD.PrescriptionDetailsQty = pd['Qty']
			prD.PrescriptionDirection = pd['Sig']
			prD.prescription_id = prId
			db.session.add(prD)
			db.session.flush()
		db.session.commit()
		handleSetResponseMessage ('create_prescription', 'Prescription Saved!', False)
	except:
		handleSetResponseMessage ('create_prescription', 'Prescription Save failed!', True)

@socketio.on('getgraph')
def handleGetGraph():
	#yearly per month checkups/visits 	#gross income
	rtotalYearVisits = 0
	monthlyPatientRaw = []
	
	rtotalYearGross = 0
	monthlyGrossRaw = []

	for m in months:
		if int(m) >= int(currentMonth):
			result = handleGetMonthlyVisits(m, currentYear)
			monthlyPatientRaw.append(result['total'])		
			rtotalYearVisits += result['total']

			monthlyGrossRaw.append(result['gross'])		
			rtotalYearGross = rtotalYearGross + result['gross']	
		else:
			monthlyPatientRaw.append(0)		
			rtotalYearVisits += 0

			monthlyGrossRaw.append(0)		
			rtotalYearGross = rtotalYearGross + 0

	patientMonthlyData = {'patientVisits' : {'year': currentYear, 'data': monthlyPatientRaw, 'yearTotal': rtotalYearVisits}, 'gross': {'year': currentYear, 'data': monthlyGrossRaw, 'yearTotal': rtotalYearGross}}
		
	

	emit('sendgraphdata', patientMonthlyData)
	
	#patients yesterday
	
	alist = []
	today = date.today()
	yesterday = today - timedelta(days = 1)
	
	for v in ClinicVisit.query.filter(ClinicVisit.ClinicVisitDate == yesterday.strftime("%Y-%m-%d")).order_by(ClinicVisit.time_created).all():
		cv = ClinicVisitSchema.dump(v).data	
		cv['ClinicVisitPhysicalExam'] = json.loads(cv['ClinicVisitPhysicalExam'])
		vd = ClinicVisitDetails.query.filter(ClinicVisitDetails.ClinicVisitDetailsId == cv['visitDetailsId']).first()
		v = ClinicVisitDetailsSchema.dump(vd).data
		print(v)
		if v['ClinicVisitDetailsStatus'] == "ok":
			p = Patient.query.filter(Patient.PatientId == cv['patientId']).first()
			pd = PatientDetails.query.filter(PatientDetails.patient_id == cv['patientId']).first()

			tmpP = PatientSchema.dump(p).data
			tmpP['patient_details'] = PatientDetailsSchema.dump(pd).data
			tmpP['patient_details']['PatientDetailsPhoto'] = "data:image/jpeg;base64," + tmpP['patient_details']['PatientDetailsPhoto']
			bd = tmpP['PatientBirthdate'].split("-")
			tmpP['PatientAge'] = calculateAge(date(int(bd[0]), int(bd[1]), int(bd[2])))
			tmpP['clinic_visit'] = cv
			tmpP['clinic_visit']['visit_details'] = v
			reqs = []
			for d in tmpP['clinic_visit']['lab_request']:
				
				req = LabRequest.query.filter(LabRequest.LabRequestId == d).first()
				r = LabRequestSchema.dump(req).data
				lr = LabTypes.query.filter(LabTypes.LabTypesId == r["labTypesId"]).first()
				d = LabTypesSchema.dump(lr).data
				r['name'] = d['LabTypesName']
				reqs.append(r)
			tmpP['clinic_visit']['lab_request'] = reqs
		
			alist.append(tmpP)
	if len(alist) == 0:
		alist = None
	emit('yesterdayappointmentlist', alist)

@socketio.on('getdailytransaction')
def handleGetDailyTransaction(date):
	print(date)
	# format = '%m/%d/%Y'
	# formatted = datetime.strptime(date, format)
	# print(formatted.date())
	visitors = handleGetDailyVisitors(date)
	print(visitors)
	emit('senddailytrans', visitors)



#NON WS FUNCTIONS
def handleGetDailyVisitors(filter):
	sql = text('select p.fname, p.mname, p.lname,p.ext, cv.date_visit, vd.charge  from clinic_visit cv left join visit_details vd on cv.visit_details_id = vd.id left join patient p on cv.patient_id = p.id where vd.status = "ok" and cv.date_visit = "'+ str(filter) +'" and vd.charge is not null')
	result = db.engine.execute(sql)
	v = []
	tvcharge = 0

	for row in result:
		vname = row[0] + ' ' +row[1] + ' ' +row[2] + ' ' + row[3]
		vdate = row[4]
		vcharge = int(row[5])
		tvcharge = tvcharge + vcharge
		vc = {'name': vname, "date": str(vdate), "charge": vcharge}
		v.append(vc)
	return {'vis':v, 'tvcharge': tvcharge}

def handleGetMonthlyVisits(month, year):
	sql = text('select count(case month(cv.date_visit) when '+ str(month) +' then 1 else null end) as visits, sum(case month(cv.date_visit) when '+ str(month) +' then vd.charge else null end) as mgross from clinic_visit cv left join visit_details vd on cv.visit_details_id = vd.id where vd.status = "ok" and year(cv.date_visit) = '+ str(currentYear) +' and vd.charge is not null ')
	result = db.engine.execute(sql)
	countres = 0
	tcharge = 0

	for row in result:
		countres = row[0]
		if not row[1]:
			tcharge = 0
		else:
			tcharge = int(row[1]) 
		
	
	return {'total': countres, 'gross': tcharge}
	 


def handleGetPreferences():
	hospital = HospitalSetupSchema.dump(HospitalSetup.query.first()).data
	clinic = ClinicSetupSchema.dump(ClinicSetup.query.first()).data
	doctor = DoctorSetupSchema.dump(DoctorSetup.query.first()).data
	pathology = []
	xray = []
	ultrasound = []
	for lr in LabTypes.query.all():
		d = LabTypesSchema.dump(lr).data
		if d['labClassificationId'] == 1:
			pathology.append({'id': d['LabTypesId'], 'value': d['LabTypesName'], 'label': d['LabTypesName'], 'class': d['labClassificationId']})
		elif d['labClassificationId'] == 2:
			xray.append({'id': d['LabTypesId'], 'value': d['LabTypesName'], 'label': d['LabTypesName'], 'class': d['labClassificationId']})
		elif d['labClassificationId'] == 3:	
			ultrasound.append({'id': d['LabTypesId'], 'value': d['LabTypesName'], 'label': d['LabTypesName'], 'class': d['labClassificationId']})

	labreqs = {'pathology': pathology, 'xray': xray, 'ultrasound': ultrasound}
	clinic['ClinicSetupSchedule'] = json.loads(clinic['ClinicSetupSchedule'])
	dump = json.dumps({'clinic': clinic, 'hospital': hospital, 'doctor': doctor, 'labreqoptions': labreqs})
	strD = base64.b64encode(dump.encode('utf-8'))

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
