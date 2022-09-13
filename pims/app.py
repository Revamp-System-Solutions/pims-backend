import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from collections import namedtuple
from .model.model import *
from sqlalchemy import desc
from datetime import datetime, timedelta
import dateparser
from .model.schema import *
import base64
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/pims'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('connect')
def handleConnect():
	now = datetime.now()
	dow = calendar.day_name[now.weekday()]
	print(dow + " Connected")
#	handleGetPatients('100')

@socketio.on('getpatients')
def handleGetPatients(d):
	plist = []
	for p in Patient.query.filter(Patient.PatientFname.like(d)).all():
		tmpP = PatientSchema.dump(p).data
		plist.append(tmpP)
		

	emit('listpatients', plist, broadcast=True)
	print(plist)
