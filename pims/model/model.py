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
	PatientBirthdate = db.Column('birthdate',DATE)
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

class HistoryType(db.Model):
	__tablename__= 'history_type'
	HistoryTypeId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	HistoryTypeName = db.Column('name', db.String(50))

class PatientHistory(db.Model):
	__tablename__= 'patient_history'
	PatientHistoryId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	patientId = db.relationship('Patient', backref='patient_history')
	PatientHistoryProcedure = db.Column('procedure', db.String(500))
	PatientHistoryResult = db.Column('result', db.String(500))
	PatientHistoryRecorded = db.Column('date',DateTime(timezone=True))
	history_type_id = db.Column(db.Integer, db.ForeignKey('history_type.id'))
	HistoryTypeId = db.relationship('HistoryType', backref='patient_history')

class PatientVaccine(db.Model):
	__tablename__= 'patient_vaccine'
	PatientVaccineId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	patientId = db.relationship('Patient', backref='patient_vaccine')
	PatientVaccineName = db.Column('name', db.String(500))
	PatientVaccineAdministered = db.Column('date_administered',DateTime(timezone=True))

class Queue(db.Model):
	__tablename__= 'history_type'
	QueueId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	QueueOrder = db.Column('order', db.String(50))
	QueuePriority = db.Column('is_priority', BOOLEAN)
	QueueDate = db.Column('date',DateTime(timezone=True))

class ClinicVisitDetails(db.Model):
	__tablename__= 'visit_details'
	ClinicVisitDetailsId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	ClinicVisitDetailsNotes = db.Column('notes', db.String(500))
	ClinicVisitDetailsPurpose = db.Column('purpose', db.String(500))
	ClinicVisitDetailsDiagnosis = db.Column('diagnosis', db.String(500))
	ClinicVisitDetailsPlan = db.Column('Plan', db.String(500))
	ClinicVisitDetailsCharge = db.Column('Charge', db.Integer)

class ClinicVisit(db.Model):
	__tablename__= 'clinic_visit'
	ClinicVisitId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	patientId = db.relationship('Patient', backref='clinic_visit')
	ClinicVisitDate = db.Column('date_visit', DateTime(timezone=True))
	ClinicVisitComplaints = db.Column('complaints', db.String(500))
	ClinicVisitVitals = db.Column('vitals', db.String(150))
	ClinicVisitInfo = db.Column('patient_info', db.String(150), default='{ "height":0, "weight":0, "head":0 }')
	visit_details_id = db.Column(db.Integer, db.ForeignKey('visit_details.id'))
	visitDetailsId = db.relationship('ClinicVisitDetails', backref='clinic_visit')
	ClinicVisitHasAppointment = db.Column('has_appointment', BOOLEAN)

# class PhysicalExam(db.Model):
# class LabClassification(db.Model):
# class LabTypes(db.Model):
# class LabRequest(db.Model):
# class PurposeSetup(db.Model):
# class Appointment(db.Model):
# class Drug(db.Model):
# class DrugDosage(db.Model):
# class PrescriptionType(db.Model):
# class Prescription(db.Model):
# class PrescriptionDetails(db.Model):
# class CertificationType(db.Model):
# class CertificationTemplate(db.Model):
# class Certification(db.Model):
# class DirectionsSetup(db.Model):
# class DoctorSetup(db.Model):
# class HospitalSetup(db.Model):
# class ClinicSetup(db.Model):
# class DailyReport(db.Model):
# class UserType(db.Model):
# class User(db.Model):
class Log(db.Model):
	__tablename__= 'logs'
	lId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	lDesc = db.Column('log_info', db.String(500))
	log_date = db.Column(DateTime(timezone=True), nullable=False)