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
class _LogSchema(ModelSchema):
	class Meta:
		model = Log

PatientSchema = _PatientSchema()
PatientDetailsSchema = _PatientDetailsSchema()
PatientHistorySchema = _PatientHistorySchema()
LogSchema = _LogSchema()