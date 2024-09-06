from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from dotenv import load_dotenv
import os
from sqlalchemy import DateTime, func
from geoalchemy2 import Geography

from .extensions import db


load_dotenv()

class Pharmacy(UserMixin, db.Model):
    __tablename__ = 'Pharmacy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Need the username, password for logging in. Usernames shouldn't overlap
    username = db.Column(db.String(255),unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    pharmacy_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    building_num = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(255), nullable=False)
    apt_num = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    coord = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)

    def get_token(self):
        serial=Serializer(os.getenv('SECRET_KEY'))
        return serial.dumps({'pharmacy_id':self.id})
    
    # This method can't access properties of Pharmacy class
    @staticmethod
    def verify_token(token, max_age=60):
        serial = Serializer(os.getenv('SECRET_KEY'))
        try:
            pharmacy_id = serial.loads(token, max_age=max_age)['pharmacy_id']
        except:
            return None
        return Pharmacy.query.get(pharmacy_id)

class Patient(UserMixin, db.Model):
    __tablename__ = 'Patient'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Need the username, password for logging in. Usernames shouldn't overlap
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    d_o_b = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    emergency_cont = db.Column(db.String(255), nullable=False)
    building_num = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(255), nullable=False)
    apt_num = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('Pharmacy.id'), nullable=False)
    insurance_url = db.Column(db.String(510))

    # Creates bi-directional relationship between Pharmacy and Patient by adding model attributes
    pharmacy = db.relationship('Pharmacy', backref='patients')

    def get_token(self):
        serial=Serializer(os.getenv('SECRET_KEY'))
        return serial.dumps({'patient_id':self.id})
    
    # This method can't access properties of Patient class
    @staticmethod
    def verify_token(token, max_age=60):
        serial = Serializer(os.getenv('SECRET_KEY'))
        try:
            patient_id = serial.loads(token, max_age=max_age)['patient_id']
        except:
            return None
        return Patient.query.get(patient_id)


class Hospital(UserMixin, db.Model):
    __tablename__ = 'Hospital'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hospital_name = db.Column(db.String(255), nullable=False)
    building_num = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(255), nullable=False)
    apt_num = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    coord = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)

class Physician(UserMixin, db.Model):
    __tablename__ = 'Physician'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Usernames shouldn't overlap, so they're unique
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('Hospital.id'), nullable=False)

    hospital = db.relationship('Hospital', backref='physicians')

    def get_token(self):
        serial=Serializer(os.getenv('SECRET_KEY'))
        return serial.dumps({'physician_id':self.id})
    
    # This method can't access properties of Physician class
    @staticmethod
    def verify_token(token, max_age=60):
        serial = Serializer(os.getenv('SECRET_KEY'))
        try:
            physician_id = serial.loads(token, max_age=max_age)['physician_id']
        except:
            return None
        return Physician.query.get(physician_id)

class Medication(db.Model):
    __tablename__ = 'Medication'
    id = db.Column(db.Integer, primary_key=True)
    medication_name = db.Column(db.String(255), nullable=False)
    side_effects = db.Column(db.String(510), nullable=False)
    instruction_vid_name = db.Column(db.String(255))
    instruction_vid_url = db.Column(db.String(510))

class Patient_medications(db.Model):
    __tablename__ = 'Patient_medications'
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('Medication.id'), primary_key=True)
    medication_name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(255), nullable=False)
    days_supply = db.Column(db.Integer, nullable=False)
    prescription_valid_till = db.Column(db.Date, nullable=False)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'), nullable=False)
    date_prescribed = db.Column(db.Date, nullable=False)
    phys_note = db.Column(db.String(510))
    next_refill_date = db.Column(db.Date)

    # Creates a bi-directional relationship between this model with both Patient and Physician
    patient = db.relationship('Patient', backref='medications')
    physician = db.relationship('Physician', backref='medications')

class Patient_allergies(db.Model):
    __tablename__ = 'Patient_allergies'
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), primary_key=True)
    allergy_name = db.Column(db.String(255), primary_key=True)

    patient = db.relationship('Patient', backref='allergies')

class Patient_diseases(db.Model):
    __tablename__ = 'Patient_diseases'
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), primary_key=True)
    disease_name = db.Column(db.String(255), primary_key=True)

class Medication_notes(db.Model):
    __tablename__ = 'Medication_notes'
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id', name='fk_med_notes_patient_id'), primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('Medication.id', name='fk_med_notes_medication_id'), primary_key=True)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id', name='fk_med_notes_physician_id'), primary_key=True)
    notes = db.Column(db.String(510), nullable=False)

class Refill_notifications(db.Model):
    __tablename__ = 'Refill_notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('Medication.id'), nullable=False)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('Pharmacy.id'), nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

class Chats(db.Model):
    __tablename__ = 'Chats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=False)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_by = db.Column(db.String(255), nullable=False)
    sent = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

class Availability(db.Model):
    __tablename__ = 'Availability'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    available_date = db.Column(db.Date, nullable=False)
    available_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'))

    patient = db.relationship('Patient', backref='appointments')
    physician = db.relationship('Physician', backref='availability')

