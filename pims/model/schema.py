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