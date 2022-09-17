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
	#print(date(2017,9,18))
	plist = []
	for p in Patient.query.filter(Patient.PatientFname.like(d)).all():
		pd = PatientDetails.query.filter(PatientDetails.patient_id == p.PatientId).first()
		tmpP = PatientSchema.dump(p).data
		tmpP['patient_details'] = PatientDetailsSchema.dump(pd).data
		bd = tmpP['PatientBirthdate'].split("-")
		tmpP['PatientAge'] = calculateAge(date(int(bd[0]), int(bd[1]), int(bd[2])))
		plist.append(tmpP)

	emit('listpatients', plist)
	print('sent')

def calculateAge(dob):
	today = date.today()
	age = today.year - dob.year -((today.month, today.day) < (dob.month, dob.day))
	return age
