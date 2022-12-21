from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
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
    __tablename__ = 'patient'
    PatientId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    PatientFname = db.Column('fname', db.String(50))
    PatientMname = db.Column('mname', db.String(50))
    PatientLname = db.Column('lname', db.String(50))
    PatientExt = db.Column('ext', db.String(10))
    PatientSex = db.Column('sex', db.String(5))
    PatientBirthdate = db.Column('birthdate', DATE)
    PatientAddress = db.Column('address', db.String(1000))
    PatientContact = db.Column('contact', db.String(20))
    PatientReligion = db.Column('religion', db.String(50))
    PatientStatus = db.Column('tag', db.String(50), default="active")

class PatientDetails(db.Model):
    __tablename__ = 'patient_details'
    PatientDetailsId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patientId = db.relationship('Patient', backref='patient_details')
    PatientDetailsFather = db.Column('father', db.String(1000))
    PatientDetailsMother = db.Column('mother', db.String(1000))
    PatientDetailsPhoto = db.Column('photo', LONGBLOB)

class ArchivePatient(db.Model):
    __tablename__ = 'patient_archives'
    PatientId = db.Column('id', db.Integer, primary_key=True)
    PatientFname = db.Column('fname', db.String(50))
    PatientMname = db.Column('mname', db.String(50))
    PatientLname = db.Column('lname', db.String(50))
    PatientExt = db.Column('ext', db.String(10))
    PatientSex = db.Column('sex', db.String(5))
    PatientBirthdate = db.Column('birthdate', DATE)
    PatientAddress = db.Column('address', db.String(1000))
    PatientContact = db.Column('contact', db.String(20))
    PatientReligion = db.Column('religion', db.String(50))
    PatientStatus = db.Column('tag', db.String(50), default="archived")

class ArchivePatientDetails(db.Model):
    __tablename__ = 'patient_details_archive'
    PatientDetailsId = db.Column('id', db.Integer, primary_key=True)
    archive_patient_id = db.Column(db.Integer)
    # patientId = db.relationship('ArchivePatient', backref='patient_details_archive')
    PatientDetailsFather = db.Column('father', db.String(1000))
    PatientDetailsMother = db.Column('mother', db.String(1000))
    PatientDetailsPhoto = db.Column('photo', LONGBLOB)

class HistoryType(db.Model):
    __tablename__ = 'history_type'
    HistoryTypeId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    HistoryTypeName = db.Column('name', db.String(50))


class PatientHistory(db.Model):
    __tablename__ = 'patient_history'
    PatientHistoryId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patientId = db.relationship('Patient', backref='patient_history')
    PatientHistoryProcedure = db.Column('procedure', db.String(1000))
    PatientHistoryResult = db.Column('result', db.String(1000))
    PatientHistoryRecorded = db.Column('date', DateTime(timezone=True))
    history_type_id = db.Column(db.Integer, db.ForeignKey('history_type.id'))
    HistoryTypeId = db.relationship('HistoryType', backref='patient_history')


class PatientVaccine(db.Model):
    __tablename__ = 'patient_vaccine'
    PatientVaccineId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patientId = db.relationship('Patient', backref='patient_vaccine')
    PatientVaccineName = db.Column('name', db.String(1000))
    PatientVaccineAdministered = db.Column('date_administered', DateTime(timezone=True))


class Queue(db.Model):
    __tablename__ = 'queue'
    QueueId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    QueueOrder = db.Column('order', db.String(50))
    QueuePriority = db.Column('is_priority', BOOLEAN)
    QueueDate = db.Column('date', DateTime(timezone=True))


class ClinicVisitDetails(db.Model):
    __tablename__ = 'visit_details'
    ClinicVisitDetailsId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    ClinicVisitDetailsNotes = db.Column('notes', db.String(1000))
    ClinicVisitDetailsPurpose = db.Column('purpose', db.String(1000))
    ClinicVisitDetailsDiagnosis = db.Column('diagnosis', db.String(1000))
    ClinicVisitDetailsPlan = db.Column('followup_plan', db.String(1000))
    ClinicVisitDetailsCharge = db.Column('charge', db.String(150), server_default="0")
    ClinicVisitDetailsStatus = db.Column('status', db.String(150), default="queueing")

class ClinicVisit(db.Model):
    __tablename__ = 'clinic_visit'
    ClinicVisitId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patientId = db.relationship('Patient', backref='clinic_visit')
    ClinicVisitDate = db.Column('date_visit', DATE)
    ClinicVisitComplaints = db.Column('complaints', db.String(1000))
    ClinicVisitPhysicalExam = db.Column('physical_exam', db.String(1000), nullable=False, server_default='{"blood_pressure": "0", "pulse_rate": "0" , "body_temp": "0", "respiration_rate": "0", "height": "0", "weight": "0", "head": "0", "skin_musculo_skeletal": "-", "abdomen_urinary": "-", "HEENTNeck": "-", "pelvic": "-", "chest_heart_lungs": "-", "neurologic": "-"}')
    visit_details_id = db.Column(db.Integer, db.ForeignKey('visit_details.id'))
    visitDetailsId = db.relationship('ClinicVisitDetails', backref='clinic_visit')
    ClinicVisitHasAppointment = db.Column('has_appointment', BOOLEAN)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())


class LabClassification(db.Model):
    __tablename__ = 'lab_classification'
    LabClassificationId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    LabClassificationName = db.Column('name', db.String(50))


class LabTypes(db.Model):
    __tablename__ = 'lab_types'
    LabTypesId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    LabTypesName = db.Column('name', db.String(50))
    lab_classification_id = db.Column(
        db.Integer, db.ForeignKey('lab_classification.id'))
    labClassificationId = db.relationship(
        'LabClassification', backref='lab_types')


class LabRequest(db.Model):
    __tablename__ = 'lab_request'
    LabRequestId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    lab_types_id = db.Column(db.Integer, db.ForeignKey('lab_types.id'))
    labTypesId = db.relationship('LabTypes', backref='lab_request')
    LabRequestResult =  db.Column('photo', LONGBLOB)
    LabRequestDate = db.Column('date_requested', DateTime(timezone=True), server_default=func.now())
    LabRequestTestDate = db.Column('date_tested', DateTime(timezone=True), onupdate=func.now())
    LabRequestBy = db.Column('requested_by', db.String(150))
    clinic_visit_id = db.Column(db.Integer, db.ForeignKey('clinic_visit.id'))
    clinicVisitId = db.relationship('ClinicVisit', backref='lab_request')


class PurposeSetup(db.Model):
    __tablename__ = 'purpose_setup'
    PurposeSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    PurposeSetupValue = db.Column('value', db.String(50))


class Drug(db.Model):
    __tablename__ = 'drug'
    DrugId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    DrugBrandName = db.Column('brand_name', db.String(100))
    DrugGenericName = db.Column('generic_name', db.String(100))
    DrugStatus = db.Column('status', db.String(10), default='active')


class DrugDosage(db.Model):
    __tablename__ = 'drug_dosage'
    DrugDosageId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drug.id'))
    drugId = db.relationship('Drug', backref='drug_dosage')
    DrugDosageDesc = db.Column('description', db.String(150))

class PrescriptionType(db.Model):
    __tablename__ = 'prescription_type'
    PrescriptionTypeId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    PrescriptionTypeName = db.Column('name', db.String(100))


class Prescription(db.Model):
    __tablename__ = 'prescription'
    PrescriptionId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patientId = db.relationship('Patient', backref='prescription')
    prescription_type_id = db.Column(db.Integer, db.ForeignKey('prescription_type.id'))
    prescriptionTypeId = db.relationship('PrescriptionType', backref='prescription')
    PrescriptionNote = db.Column('note', db.String(1000))


class PrescriptionDetails(db.Model):
    __tablename__ = 'prescription_details'
    PrescriptionDetailsId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drug.id'))
    drugId = db.relationship('Drug', backref='prescription_details')
    dosage_id = db.Column(db.Integer, db.ForeignKey('drug_dosage.id'))
    dosageId = db.relationship('DrugDosage', backref='prescription_details')
    PrescriptionDetailsQty = db.Column('qty', db.Integer)
    PrescriptionDirection = db.Column('direction', db.String(1000))
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'))
    prescriptionId = db.relationship('Prescription', backref='prescription_details')


class CertificationType(db.Model):
    __tablename__ = 'certification_type'
    CertificationTypeId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    CertificationTypeName = db.Column('name', db.String(100))
    # CertificationTypeFormat = db.Column('format', db.String(1000))


class CertificationTemplate(db.Model):
    __tablename__ = 'certification_template'  
    CertificationTemplateId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    certification_type_id = db.Column(db.Integer, db.ForeignKey('certification_type.id'))
    certificationTypeId = db.relationship('CertificationType', backref='certification_template')
    CertificationTemplateContent = db.Column('content', LONGTEXT)


class Certification(db.Model):
    __tablename__ = 'certification'
    CertificationId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patientId = db.relationship('Patient', backref='certification')
    certification_template_id = db.Column(db.Integer, db.ForeignKey('certification_template.id'))
    certificationTemplateId = db.relationship('CertificationTemplate', backref='certification')


class DirectionsSetup(db.Model):
    __tablename__ = 'directions_setup'
    DirectionsSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    DirectionsSetupContent = db.Column('content', db.String(200))


class DoctorSetup(db.Model):
    __tablename__ = 'doctor_setup'
    DoctorSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    DoctorSetupName = db.Column('name', db.String(200))
    DoctorSetupLic = db.Column('license', db.String(200))
    DoctorSetupS2 = db.Column('s2', db.String(200))
    DoctorSetupPtr = db.Column('ptr', db.String(200))
    DoctorSetupMembership = db.Column('membership', db.String(200))
    DoctorSetupMembershipBody = db.Column('recognizing_body', db.String(200))


class HospitalSetup(db.Model):
    __tablename__ = 'hospital_setup'
    HospitalSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    HospitalSetupName = db.Column('name', db.String(100))
    HospitalSetupAddress = db.Column('address', db.String(200))


class ClinicSetup(db.Model):
    __tablename__ = 'clinic_setup'
    ClinicSetupId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    ClinicSetupName = db.Column('name', db.String(100))
    ClinicSetupAddress = db.Column('address', db.String(200))
    ClinicSetupSchedule = db.Column('clinic_hours', LONGTEXT)
    hospital_setup_id = db.Column(db.Integer, db.ForeignKey('hospital_setup.id'))
    hospitalSetupId = db.relationship('HospitalSetup', backref='clinic_setup')


class DailyReport(db.Model):
    __tablename__ = 'daily_report'
    DailyReportId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    DailyReportTotalClients = db.Column('total_clients', db.String(500), nullable=False, default='{ "walkins" : 0, "appointments" : 0 }')
    DailyReportTotalCharges = db.Column('total_charges', DOUBLE)


class UserType(db.Model):
    __tablename__ = 'user_type'
    UserTypeId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    UserTypeName = db.Column('type', db.String(50))


class User(db.Model):
    __tablename__ = 'user'
    UserId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    UserFname = db.Column('fname', db.String(100))
    UserLname = db.Column('lname', db.String(100))
    UserNickname = db.Column('nickname', db.String(100))
    UserUname = db.Column('username', db.String(100), unique=True)
    UserPassword = db.Column('password', db.String(100))
    UserRole = db.Column('role', db.String(50))
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    userTypeId = db.relationship('UserType', backref='user')


class Log(db.Model):
    __tablename__ = 'logs'
    lId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    lDesc = db.Column('log_info', db.String(1000))
    log_date = db.Column(DateTime(timezone=True), nullable=False)
