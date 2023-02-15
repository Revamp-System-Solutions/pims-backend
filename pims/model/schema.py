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

class _PatientCardsSchema(ModelSchema):
    class Meta:
        model = PatientCards

class _ArchivePatientSchema(ModelSchema):
    class Meta:
        model = ArchivePatient

class _ArchivePatientDetailsSchema(ModelSchema):
    class Meta:
        model = ArchivePatientDetails

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

class _LabClassificationSchema(ModelSchema):
    class Meta:
        model = LabClassification

class _LabTypesSchema(ModelSchema):
    class Meta:
        model = LabTypes
class _LabClassificationChildSchema(ModelSchema):
    class Meta:
        model = LabClassificationChild        

class _LabRequestSchema(ModelSchema):
    class Meta:
        model = LabRequest

class _PurposeSetupSchema(ModelSchema):
    class Meta:
        model = PurposeSetup

class _DrugSchema(ModelSchema):
    class Meta:
        model = Drug

class _DrugDosageSchema(ModelSchema):
    class Meta:
        model = DrugDosage


class _PrescriptionTypeSchema(ModelSchema):
    class Meta:
        model = PrescriptionType


class _PrescriptionSchema(ModelSchema):
    class Meta:
        model = Prescription


class _PrescriptionDetailsSchema(ModelSchema):
    class Meta:
        model = PrescriptionDetails


class _CertificationTypeSchema(ModelSchema):
    class Meta:
        model = CertificationType


class _CertificationTemplateSchema(ModelSchema):
    class Meta:
        model = CertificationTemplate


class _CertificationSchema(ModelSchema):
    class Meta:
        model = Certification


class _DirectionsSetupSchema(ModelSchema):
    class Meta:
        model = DirectionsSetup


class _DoctorSetupSchema(ModelSchema):
    class Meta:
        model = DoctorSetup


class _HospitalSetupSchema(ModelSchema):
    class Meta:
        model = HospitalSetup


class _ClinicSetupSchema(ModelSchema):
    class Meta:
        model = ClinicSetup


class _DailyReportSchema(ModelSchema):
    class Meta:
        model = DailyReport


class _UserTypeSchema(ModelSchema):
    class Meta:
        model = UserType


class _UserSchema(ModelSchema):
    class Meta:
        model = User


class _LogSchema(ModelSchema):
    class Meta:
        model = Log

PatientCardsSchema = _PatientCardsSchema()
LabClassificationSchema = _LabClassificationSchema()
LabTypesSchema = _LabTypesSchema()
LabClassificationChildSchema = _LabClassificationChildSchema()
LabRequestSchema = _LabRequestSchema()
PurposeSetupSchema = _PurposeSetupSchema()
DrugSchema = _DrugSchema()
DrugDosageSchema = _DrugDosageSchema()
PrescriptionTypeSchema = _PrescriptionTypeSchema()
PrescriptionSchema = _PrescriptionSchema()
PrescriptionDetailsSchema = _PrescriptionDetailsSchema()
CertificationTypeSchema = _CertificationTypeSchema()
CertificationTemplateSchema = _CertificationTemplateSchema()
CertificationSchema = _CertificationSchema()
DirectionsSetupSchema = _DirectionsSetupSchema()
DoctorSetupSchema = _DoctorSetupSchema()
HospitalSetupSchema = _HospitalSetupSchema()
ClinicSetupSchema = _ClinicSetupSchema()
DailyReportSchema = _DailyReportSchema()
UserTypeSchema = _UserTypeSchema()
UserSchema = _UserSchema()
HistoryTypeSchema = _HistoryTypeSchema()
PatientVaccineSchema = _PatientVaccineSchema()
QueueSchema = _QueueSchema()
ClinicVisitSchema = _ClinicVisitSchema()
ClinicVisitDetailsSchema = _ClinicVisitDetailsSchema()
PatientSchema = _PatientSchema()
PatientDetailsSchema = _PatientDetailsSchema()
ArchivePatientSchema = _ArchivePatientSchema()
ArchivePatientDetailsSchema = _ArchivePatientDetailsSchema()
PatientHistorySchema = _PatientHistorySchema()
LogSchema = _LogSchema()
