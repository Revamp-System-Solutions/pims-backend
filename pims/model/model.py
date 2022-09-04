from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.dialects.mysql import \
		BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
		DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
		LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
		NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
		TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

db = SQLAlchemy()

class Patient(db.Model):
	__tablename__= 'patient'
	PatientId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	PatientFname = db.Column('fname', db.String(50))
	PatientMname = db.Column('mname', db.String(50))
	PatientLname = db.Column('lname', db.String(50))
	PatientExt = db.Column('ext', db.String(10))
	PatientSex = db.Column('sex', db.String(5))
	PatientBirthdate = db.Column('birthdate',DateTime(timezone=True))
	PatientAddress = db.Column('address', db.String(500))
	PatientContact = db.Column('contact', db.String(20))
	PatientReligion = db.Column('religion', db.String(50))

class PatientDetails(db.Model):
	__tablename__= 'patient_details'
	PatientDetailsId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	patientId = db.relationship('Patient', backref='patient_details')
	PatientDetailsFather = db.Column('father', db.String(500))
	PatientDetailsFather = db.Column('father', db.String(500)) 
	PatientDetailsPhoto = db.Column('photo', db.String(150))

class PatientHistory(db.Model):
	__tablename__= 'patient_history'
	PatientHistoryId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	patientId = db.relationship('Patient', backref='patient_history')
	PatientHistoryProcedure = db.Column('procedure', db.String(500))
	PatientHistorResult = db.Column('result', db.String(500))
	PatientHistoryRecorded = db.Column('date',DateTime(timezone=True))

class Log(db.Model):
	__tablename__= 'logs'
	lId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	lDesc = db.Column('log_info', db.String(500))
	log_date = db.Column(DateTime(timezone=True), nullable=False)