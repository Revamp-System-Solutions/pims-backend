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
	__tablename__= 'queue'
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
	ClinicVisitInfo = db.Column('patient_info', db.String(150), nullable=False, default='{ "height":0, "weight":0, "head":0 }')
	visit_details_id = db.Column(db.Integer, db.ForeignKey('visit_details.id'))
	visitDetailsId = db.relationship('ClinicVisitDetails', backref='clinic_visit')
	ClinicVisitHasAppointment = db.Column('has_appointment', BOOLEAN)
	ClinicVisitPhysicalExam = db.Column('physical_exam', db.String(500))

class LabClassification(db.Model):
	__tablename__= 'lab_classification'
	LabClassificationId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	LabClassificationName = db.Column('name', db.String(50))

class LabTypes(db.Model):
	__tablename__= 'lab_types'
	LabTypesId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	LabTypesName = db.Column('name', db.String(50))
	lab_classification_id = db.Column(db.Integer, db.ForeignKey('lab_classification.id'))
	labClassificationId = db.relationship('LabClassification', backref='lab_types')

class LabRequest(db.Model):
	__tablename__= 'lab_request'
	LabRequestId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	lab_types_id = db.Column(db.Integer, db.ForeignKey('lab_types.id'))
	labTypesId = db.relationship('LabTypes', backref='lab_request')
	LabRequestResult = db.Column('result', db.String(500))
	LabRequestDate = db.Column('date_requested',DateTime(timezone=True))
	LabRequestTestDate = db.Column('date_tested',DateTime(timezone=True))
	LabRequestBy = db.Column('requested_by', db.String(150))
	clinic_visit_id = db.Column(db.Integer, db.ForeignKey('clinic_visit.id'))
	clinicVisitId = db.relationship('ClinicVisit', backref='lab_request')

class PurposeSetup(db.Model):
	__tablename__= 'purpose_setup'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	PurposeSetupValue = db.Column('value', db.String(50))

class Drug(db.Model):
	__tablename__= 'drug'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class DrugDosage(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class PrescriptionType(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class Prescription(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class PrescriptionDetails(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class CertificationType(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class CertificationTemplate(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class Certification(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class DirectionsSetup(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class DoctorSetup(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class HospitalSetup(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class ClinicSetup(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class DailyReport(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class UserType(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
# class User(db.Model):
	__tablename__= 'history_type'
	PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)

class Log(db.Model):
	__tablename__= 'logs'
	lId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	lDesc = db.Column('log_info', db.String(500))
	log_date = db.Column(DateTime(timezone=True), nullable=False)