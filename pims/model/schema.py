from .model import *
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import base64

class _PatientSchema(ModelSchema):
	class Meta:
		model = Patient
class _PatientDetailsSchema(ModelSchema):
	class Meta:
		model = PatientDetails
class _PatientHistorySchema(ModelSchema):
	class Meta:
		model = PatientHistory
class _HistoryTypeSchema(ModelSchema):
	class Meta:
		model = HistoryType
class _PatientVaccineSchema(ModelSchema):
	class Meta:
		model = PatientVaccine
class _QueueSchema(ModelSchema):
	class Meta:
		model = Queue
class _ClinicVisitSchema(ModelSchema):
	class Meta:
		model = ClinicVisit
class _ClinicVisitDetailsSchema(ModelSchema):
	class Meta:
		model = ClinicVisitDetails
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

class _LogSchema(ModelSchema):
	class Meta:
		model = Log
HistoryTypeSchema = _HistoryTypeSchema()
PatientVaccineSchema = _PatientVaccineSchema()
QueueSchema = _QueueSchema()
ClinicVisitSchema = _ClinicVisitSchema()
ClinicVisitDetailsSchema = _ClinicVisitDetailsSchema()
PatientSchema = _PatientSchema()
PatientDetailsSchema = _PatientDetailsSchema()
PatientHistorySchema = _PatientHistorySchema()
LogSchema = _LogSchema()