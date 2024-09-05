from flask import render_template, jsonify, session, send_from_directory, redirect, url_for, request, flash, Blueprint
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_, func, and_, inspect
from flask_mail import Message
from werkzeug.utils import secure_filename
import re   # imported to help find pattern in url
import os
from datetime import date, timedelta, datetime
from cryptography.fernet import Fernet

from google.cloud import storage
from . import socketio


from .db_classes import *
from .extensions import login, db, mail, admin, bcrypt
from .forms import *
from .routing_protection import *


main = Blueprint("main", __name__)

from flask_admin.contrib.sqla import ModelView
class NewView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Patient_medications).mapper.column_attrs]

admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Pharmacy, db.session))
admin.add_view(ModelView(Physician, db.session))
admin.add_view(NewView(Patient_medications, db.session))
admin.add_view(ModelView(Medication, db.session))
admin.add_view(ModelView(Availability, db.session))


# authenticates specific user login based on id number
@login.user_loader
def load_user(user_id):
    if Patient.query.filter_by(id=user_id).first():
        return Patient.query.get(user_id)
    elif Physician.query.filter_by(id=user_id).first():
        return Physician.query.get(user_id)
    elif Pharmacy.query.filter_by(id=user_id).first():
        return Pharmacy.query.get(user_id)


@main.route('/login', methods=['GET','POST'])
def login():
    if 'usertype' in session:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_mapping = {
            'patient': Patient,
            'pharmacy': Pharmacy,
            'physician': Physician
        }
        user_type = user_mapping.get(form.user.data)
        user = user_type.query.filter_by(username=form.username.data).first()
        try:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['logged_in'] = True
                if type(user) == type(Patient.query.filter_by().first()):
                    session['usertype'] = 'patient'
                    return redirect(url_for('main.patient', patient_id=user.id))
                if type(user) == type(Physician.query.filter_by().first()):
                    session['usertype'] = 'physician'
                    return redirect(url_for('main.physician'))
                if type(user) == type(Pharmacy.query.filter_by().first()):
                    session['usertype'] = 'pharmacy'
                    return redirect(url_for('main.pharmacy'))
        except:
            flash('Login not found', category='danger')
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    if session.get('logged_in'):
        session['logged_in'] = False
        session.pop('usertype')
    return redirect(url_for('main.login'))

def reset_email(user):
    token = user.get_token()
    msg = Message('Reset Password Request', recipients=[user.email], sender='noreply@mediconnect.com')
    msg.body = f''' This is your password reset request link
    To proceed, please click on the following link:

    {url_for('main.forgot_token', token=token, _external=True)}

    '''
    mail.send(msg)

@main.route('/forgot', methods=['POST','GET'])
def forgot():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user_mapping = {
            'patient': Patient,
            'pharmacy': Pharmacy,
            'physician': Physician
        }
        user_type = user_mapping.get(form.user.data)
        user = user_type.query.filter_by(email=form.email.data).first()
        if user:
            reset_email(user)
            flash('[Request has been sent to your email]')
            return redirect(url_for('main.login'))
        else:
            flash('[This email is not associated with this type of account]')
    return render_template('forgot.html', form=form)

@main.route('/forgot/<token>', methods=['POST','GET'])
def forgot_token(token):
    user_list, verified_user = [Patient, Pharmacy, Physician], None
    for user_type in user_list:
        user = user_type.verify_token(token)
        if user:
            verified_user = user

    if verified_user is None:
        flash('Invalid/expired token. Please try again')
        return redirect(url_for('main.forgot'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        verified_user.password = form.password.data
        db.session.commit()
        flash('You have successfully changed your password!')
        return redirect(url_for('main.login'))
    return render_template('change_password.html', form=form)

# FUNCTIONS

def upload_to_bucket(data, file_path, bucket_name):
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)

        # bucket.iam_configuration.uniform_bucket_level_access_enabled = False
        # bucket.patch()

        blob = bucket.blob(data)
        # blob.encryption_key(os.getenv('ENCRYPTION_KEY').encode())
        blob.upload_from_filename(file_path)
        blob.make_public()

        return blob.public_url
    except Exception as err:
        print(f'Error: {err}')

# for insurance card upload
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in {'png','pdf','jpg','jpeg','gif'}

# get coordinates of home pharmacy for specific patient (maps.html)
@main.route('/get_coordinates_spec/<int:patient_id>', methods=['GET'])
def get_coordinates_spec(patient_id):
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:
            pharmacy_coords = db.session.query(
                Pharmacy.id.label('id'),
                func.ST_X(Pharmacy.coord).label('latitude'),
                func.ST_Y(Pharmacy.coord).label('longitude'),
                Pharmacy.phone_number.label('phone_number'),
                Pharmacy.pharmacy_name.label('pharmacy_name'),
                Pharmacy.building_num.label('building_num'),
                Pharmacy.street_name.label('street_name'),
                # Pharmacy.apt_num.label('apt_num'),
                Pharmacy.city.label('city'),
                Pharmacy.state.label('state'),
                Pharmacy.zip_code.label('zip_code')
            ).filter_by(id=patient.pharmacy_id).first()
            if pharmacy_coords:
                return jsonify({"latitude": pharmacy_coords.latitude, "longitude": pharmacy_coords.longitude, "phone_number": pharmacy_coords.phone_number, "pharmacy_name": pharmacy_coords.pharmacy_name, "building_num": pharmacy_coords.building_num, "street_name": pharmacy_coords.street_name, "city": pharmacy_coords.city, "state": pharmacy_coords.state, "zip_code": pharmacy_coords.zip_code, "id":pharmacy_coords.id }), 200
            else:
                return jsonify({"error": "Coordinates not found"}), 404
        else:
            return jsonify({"error": "Patient not found"}), 404
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

# get coordinates of all pharmacies (maps.html)
@main.route('/get_coordinates_all', methods=['GET'])
def get_coordinates_all():
    try:
        pharmacy_coords = db.session.query(
            Pharmacy.id.label('id'),
            func.ST_X(Pharmacy.coord).label('latitude'),
            func.ST_Y(Pharmacy.coord).label('longitude'),
            Pharmacy.phone_number.label('phone_number'),
            Pharmacy.pharmacy_name.label('pharmacy_name'),
            Pharmacy.building_num.label('building_num'),
            Pharmacy.street_name.label('street_name'),
            # Pharmacy.apt_num.label('apt_num'),
            Pharmacy.city.label('city'),
            Pharmacy.state.label('state'),
            Pharmacy.zip_code.label('zip_code')
        ).all()
        if pharmacy_coords:
            coords_list = [{"latitude": pharmacy.latitude, "longitude": pharmacy.longitude, "phone_number": pharmacy.phone_number, "pharmacy_name": pharmacy.pharmacy_name, "building_num": pharmacy.building_num, "street_name": pharmacy.street_name, "city": pharmacy.city, "state": pharmacy.state, "zip_code": pharmacy.zip_code, "id": pharmacy.id} for pharmacy in pharmacy_coords]       
            return jsonify(coords_list), 200
        else:
            return jsonify({"error": "Coordinates not found"}), 404
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

# get a patient's medication list (patient.html)
@main.route('/get_patient_medications/<int:patient_id>', methods=['GET'])
@protected_route
def get_patient_medications(patient_id):
    try:
        patient_meds = db.session.query(
            Patient_medications.medication_id.label('medication_id'),
            Patient_medications.dosage.label('dosage'),
            Patient_medications.frequency.label('frequency'),
            Patient_medications.days_supply.label('days_supply'),
            Patient_medications.prescription_valid_till.label('prescription_valid_till'),
            Patient_medications.physician_id.label('physician_id'),
            Patient_medications.date_prescribed.label('date_prescribed'),
            Patient_medications.phys_note.label('phys_note'),
        ).filter_by(patient_id=patient_id).all()
        if patient_meds:
            today = date.today()
            curr_meds = []
            past_meds = []
            for med in patient_meds:
                physician_info = db.session.query(
                    Physician.first_name.label('first_name'),
                    Physician.last_name.label('last_name'),
                ).filter_by(id=med.physician_id).first()
                med_info = db.session.query(
                    Medication.medication_name.label('medication_name'),
                    Medication.side_effects.label('side_effects'),
                    Medication.instruction_vid_name.label('instruction_vid_name'),
                    Medication.instruction_vid_url.label('instruction_vid_url'),
                ).filter_by(id=med.medication_id).first()
                if today < med.prescription_valid_till:
                    curr_meds.append({"medication_name": med_info.medication_name, "dosage": med.dosage, "frequency": med.frequency, "days_supply": med.days_supply, "prescription_valid_till": med.prescription_valid_till.strftime("%m-%d-%Y"), "first_name": physician_info.first_name, "last_name": physician_info.last_name, "date_prescribed": med.date_prescribed.strftime("%m-%d-%Y"), "side_effects": med_info.side_effects, "instruction_vid_name": med_info.instruction_vid_name, "instruction_vid_url": med_info.instruction_vid_url, "phys_note": med.phys_note, "id": med.medication_id})
                else:
                    past_meds.append({"medication_name": med_info.medication_name, "dosage": med.dosage, "frequency": med.frequency, "days_supply": med.days_supply, "prescription_valid_till": med.prescription_valid_till.strftime("%m-%d-%Y"), "first_name": physician_info.first_name, "last_name": physician_info.last_name, "date_prescribed": med.date_prescribed.strftime("%m-%d-%Y"), "side_effects": med_info.side_effects, "instruction_vid_name": med_info.instruction_vid_name, "instruction_vid_url": med_info.instruction_vid_url, "phys_note": med.phys_note, "id": med.medication_id})
            return jsonify([curr_meds, past_meds]), 200
        else:
            print("No medications for this patient")
            return jsonify([[],[]]), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500
    
# get all physicians associated with a patient
@main.route('/get_patients_physicians/<int:patient_id>', methods=['GET'])
@protected_route
@patient_protected_route
def get_patients_physicians(patient_id):
    try:
        patient_meds = Patient_medications.query.filter_by(patient_id=patient_id).all()
        phys_ids = set()
        for med in patient_meds:
            phys_ids.add(med.physician_id)
        physicians = []
        for id in phys_ids:
            physician = Physician.query.filter_by(id=id).first()
            phys_info = {
                "first_name": physician.first_name,
                "last_name": physician.last_name,
                "id": id
            }      
            physicians.append(phys_info) 
        return jsonify(physicians), 200 
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500
    
# get all patients associated with a physicians
def get_physicians_patients(physician_id):
    try:
        patient_meds = Patient_medications.query.filter_by(physician_id=physician_id).all()
        pat_ids = set()
        for med in patient_meds:
            pat_ids.add(med.patient_id)
        patients = []
        for id in pat_ids:
            patient = Patient.query.filter_by(id=id).first()
            pat_info = {
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "id": id
            }      
            patients.append(pat_info) 
        return jsonify(patients), 200 
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

# get a patient's personal information, allergies, and diseases (patientInfo.html)
@main.route('/get_patient_info/<int:patient_id>', methods=['GET'])
@protected_route
def get_patient_info(patient_id):
    try:
        # fetch the patient object directly using the provided patient_id
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:
            # since you already have the "patient" object, you can directly access its attributes
            patient_info = [{
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "d_o_b": patient.d_o_b.isoformat(),
                "sex": patient.sex,
                "emergency_cont": patient.emergency_cont,
                "phone_number": patient.phone_number,
                "building_num": patient.building_num,
                "apt_num": patient.apt_num,
                "street_name": patient.street_name,
                "city": patient.city,
                "state": patient.state,
                "zip_code": patient.zip_code,
                "insurance_url":patient.insurance_url,
                "pharmacy_id": patient.pharmacy_id
            }]
            allergies = Patient_allergies.query.filter_by(patient_id=patient_id).all()
            if allergies:
                allergies_list = [{"allergy_name": allergy.allergy_name} for allergy in allergies] if allergies else []
                diseases = Patient_diseases.query.filter_by(patient_id=patient_id).all()
                if diseases:
                    diseases_list = [{"disease_name": disease.disease_name} for disease in diseases] if diseases else []
                    pharmacy = Pharmacy.query.filter_by(id=patient_info[0]["pharmacy_id"]).first()
                    if pharmacy:
                        pharmacy_list = [{"pharmacy_name": pharmacy.pharmacy_name,  "building_num": pharmacy.building_num, "street_name": pharmacy.street_name, "city": pharmacy.city, "state": pharmacy.state, "zip_code": pharmacy.zip_code}]
                        return jsonify({"patient_info": patient_info, "allergies": allergies_list, "diseases": diseases_list, "pharmacy": pharmacy_list}), 200
                    else:
                        return jsonify({"patient_info": patient_info, "allergies": allergies_list, "diseases": diseases_list, "pharmacy": []}), 200
                else:
                    return jsonify({"patient_info": patient_info, "allergies": allergies_list, "diseases": [], "pharmacy": []}), 200
            else:
                return jsonify({"patient_info": patient_info, "allergies": [], "diseases": [], "pharmacy": []}), 200
        else:
            # no patient_info
            return jsonify([]), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

# get patient's for physician's auto refill list
@main.route('/get_patient_refills', methods=['GET'])
@pharmacy_protected_route
@protected_route
def get_patient_refills():
    try:
        today = date.today()
        refills = Patient_medications.query.filter(today < Patient_medications.prescription_valid_till).all()
        results = []
        if refills:
            for refill in refills:
                if refill.next_refill_date is None or refill.next_refill_date < today:
                    date_prescribed = refill.date_prescribed
                    days_supply = refill.days_supply
                    next_refill_date = date_prescribed + timedelta(days=days_supply)
                    while (next_refill_date < refill.prescription_valid_till):
                        if next_refill_date > today:
                            break
                        else:
                            next_refill_date += timedelta(days=days_supply)
                    refill.next_refill_date = next_refill_date
                    db.session.commit()
                patient = db.session.query(
                    Patient.first_name.label('first_name'),
                    Patient.last_name.label('last_name'),
                    Patient.pharmacy_id.label('pharmacy_id')
                ).filter_by(id=refill.patient_id).first()

                res = {
                    "patient_id": refill.patient_id,
                    "medication_id": refill.medication_id,
                    "medication_name": refill.medication_name,
                    "dosage": refill.dosage,
                    "frequency": refill.frequency,
                    "days_supply": refill.days_supply,
                    "prescription_valid_till": refill.prescription_valid_till.strftime("%m-%d-%Y"),
                    "date_prescribed": refill.date_prescribed.strftime("%m-%d-%Y"),
                    "next_refill_date": refill.next_refill_date.strftime("%m-%d-%Y"),
                    "patient_name": f"{patient.first_name} {patient.last_name}",
                    "pharmacy_id": patient.pharmacy_id
                }
                
                results.append(res)
            results.sort(key=lambda x: datetime.strptime(x['next_refill_date'], '%m-%d-%Y'))
            return jsonify(results), 200
        else:
            print("No medications to refill")
            return jsonify([]), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

@main.route('/notify_refill/<int:patient_id>/<int:med_id>/<int:pharmacy_id>', methods=['GET'])
@pharmacy_protected_route
def notify_refill(patient_id, med_id, pharmacy_id):
    try:
        new_alert = Refill_notifications(patient_id=patient_id, medication_id=med_id, pharmacy_id=pharmacy_id)
        db.session.add(new_alert)
        db.session.commit()
        # emit('new_notification', {'message': 'Your medication has been refilled!'}, room=patient_id)
        return jsonify({"success": "Message was successfully uploaded"}), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

@main.route('/get_alerts', methods=['GET'])
@protected_route
def get_alerts(patient_id):
    try:
        alerts = Refill_notifications.query.filter_by(patient_id=patient_id).all()
        unread_ids = [alert.id for alert in alerts if not alert.is_read]
        alerts_data = []
        for alert in alerts:
            medication = Medication.query.filter_by(id=alert.medication_id).first()
            pharmacy = Pharmacy.query.filter_by(id=alert.pharmacy_id).first()
            if  alert.is_read is False:
                is_unread = 'unread'
            else:
                is_unread = 'read'
            alerts_data.append({'med_name': medication.medication_name, 'pharmacy_name': pharmacy.pharmacy_name, "building_num": pharmacy.building_num, "street_name": pharmacy.street_name, "city": pharmacy.city, "state": pharmacy.state, "zip_code": pharmacy.zip_code, 'is_read': is_unread, 'created_at': alert.created_at})
        Refill_notifications.query.filter(Refill_notifications.id.in_(unread_ids)).update({'is_read': True}, synchronize_session='fetch')
        db.session.commit()
        alerts_data.sort(key=lambda x: x['created_at'], reverse=True)
        return jsonify(alerts_data), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

def get_calendar_patient(patient_id, physicians):
    try:
        appointments = []
        for physician in physicians:
            physician_id = physician['id']
            physician = Physician.query.get(physician_id)
            availability = physician.availability
            for entry in availability:
                if entry.status == 'available':
                    color = 'blue'
                elif entry.status == 'requested' and entry.patient_id == int(patient_id):
                    color = 'red'
                elif entry.status == 'appointment' and entry.patient_id == int(patient_id):
                    color = 'green'
                else:
                    continue
                appt = {
                    'title': f"{physician.first_name} {physician.last_name}",
                    'start': f"{entry.available_date.strftime('%Y-%m-%d')}T{entry.available_time.strftime('%H:%M:%S')}",
                    'color': color,
                    'id': entry.id
                }
                appointments.append(appt)
        return jsonify(appointments), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

def get_calendar_physician(physician_id):
    try:
        appointments = []
        physician = Physician.query.get(physician_id)
        availability = physician.availability
        for entry in availability:
            if entry.status == 'available':
                appt = {
                    'title': "Available Appointment",
                    'start': f"{entry.available_date.strftime('%Y-%m-%d')}T{entry.available_time.strftime('%H:%M:%S')}",
                    'color': 'blue',
                    'id': entry.id
                }
            elif entry.status == 'requested':
                patient_id = entry.patient_id
                patient = Patient.query.get(patient_id)
                appt = {
                    'title': f"{patient.first_name} {patient.last_name}",
                    'start': f"{entry.available_date.strftime('%Y-%m-%d')}T{entry.available_time.strftime('%H:%M:%S')}",
                    'color': 'red',
                    'id': entry.id
                }
            else:
                # appointment
                patient_id = entry.patient_id
                patient = Patient.query.get(patient_id)
                appt = {
                    'title': f"{patient.first_name} {patient.last_name}",
                    'start': f"{entry.available_date.strftime('%Y-%m-%d')}T{entry.available_time.strftime('%H:%M:%S')}",
                    'color': 'green',
                    'id': entry.id
                }
            appointments.append(appt)
        return jsonify(appointments), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

# update a refill statuss
@pharmacy_protected_route
def update_refill(patient_id, med_id, pharmacy_id):
    try:
        pat_refill = Patient_medications.query.filter(and_(Patient_medications.patient_id==patient_id, Patient_medications.medication_id==med_id)).first()
        if pat_refill:
            next_refill_date = pat_refill.next_refill_date
            next_refill_date = next_refill_date + timedelta(days=pat_refill.days_supply)
            pat_refill.next_refill_date = next_refill_date
            db.session.commit()
            response, status_code = notify_refill(patient_id, med_id, pharmacy_id)
            if status_code == 200:
                return jsonify("success"), 200
            else:
                return response, status_code
        else:
            print("No patient with this medication ID/patient ID combination exists")
            return jsonify({"error": "No patient exists"}), 400
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500



# WORKING HERE
@main.route('/physicianPatientDetails', methods=['POST','GET'])
@physician_protected_route
def physicianPatientDetails():
    patient_id = request.args.get('patient_id')
    response, status_code = get_patient_info(patient_id)
    if status_code == 200:
        data = response.get_json()
        patient_info = data.get('patient_info')
        return render_template('users/physicianPatientDetails.html', patient_id=patient_id, patient_info=patient_info)
    else:
        return redirect(url_for("index"))

@main.route('/get_patient_notes', methods=['GET'])
@physician_protected_route
def get_patient_notes():
    results = {}
    patient_id = request.args.get("patient_id")
    medication_id = request.args.get("medication_id")
    notes = Medication_notes.query.filter_by(patient_id=patient_id).filter_by(medication_id=medication_id).all()
    for note in notes:
        result = {
            "patient_id": note.patient_id,
            "medication_id": note.medication_id,
            "note": note.notes
        }
        results[str(note.physician_id)] = result
    return jsonify(results) 

@main.route('/update_note', methods=['POST'])
@physician_protected_route
def update_note():
    patient_id = request.form.get("patient_id")
    medication_id = request.form.get("medication_id")
    physician_id = current_user.id
    notes = request.form.get("notes")
    if patient_id == None or medication_id == None or physician_id == None or notes == None:
        print(patient_id, medication_id, physician_id, notes)
        return jsonify({'status': False})
    note_exist = Medication_notes.query.filter_by(patient_id=patient_id).filter_by(medication_id=medication_id).filter_by(physician_id=physician_id).first()
    if note_exist:
        print("note exists!")
        note_exist.notes = notes
    else:
        print("note does not exist!")
        new_note = Medication_notes(patient_id=patient_id, medication_id=medication_id, physician_id=physician_id, notes=notes)
        db.session.add(new_note)
    db.session.commit()
    return jsonify({'status': True})

@main.route('/delete_notes') # temporary function for testing ################################################
@physician_protected_route
def delete_notes():
    notes_to_delete = Medication_notes.query.filter_by(physician_id=current_user.id).all()
    if notes_to_delete:
        for note in notes_to_delete:
            db.session.delete(note)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/get_physician_info/<int:physician_id>', methods=['GET'])
def get_physician_info(physician_id):
    try:
        physician = Physician.query.filter_by(id=physician_id).first()
        if not physician:
            return jsonify({'success': False, 'message': 'Physician not found'}), 404
        physician_info = {
            'success': True,
            'first_name': physician.first_name,
            'last_name': physician.last_name,
        }
        return jsonify(physician_info)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@main.route('/get_medication_list', methods=['GET'])
@physician_protected_route
def get_medication_list():
    result = {}
    medications = Medication.query.all()
    for medication in medications:
        result[medication.medication_name] = medication.id
    return jsonify(result)

@main.route('/update_medication', methods=['POST'])
@physician_protected_route
def update_medication():
    if request.method == 'POST':
        patient_id = request.args.get('patient_id')
        medication_name = request.form['medicationName']
        medication_id = Medication.query.filter_by(medication_name=medication_name).first().id
        dose = request.form['dose']
        frequency = request.form['frequency']
        daysSupply = request.form['daysSupply']
        validTill = request.form['validTill']
        medicationDate = request.form['medicationDate']
        phys_note = request.form['physNote']
        medication_exist = Patient_medications.query.filter_by(patient_id=patient_id).filter_by(medication_name=medication_name).first()
        if medication_exist:
            medication_exist.medication_id = medication_id
            medication_exist.dosage = dose
            medication_exist.frequency = frequency
            medication_exist.days_supply = daysSupply
            medication_exist.prescription_valid_till = validTill
            medication_exist.date_prescribed = medicationDate
            medication_exist.phys_note = phys_note
        else:
            new_medication = Patient_medications(
                patient_id=patient_id,
                medication_id=medication_id,
                medication_name=medication_name, 
                dosage=dose, 
                frequency=frequency, 
                days_supply=daysSupply,
                prescription_valid_till=validTill,
                physician_id=current_user.id, 
                date_prescribed=medicationDate,
                phys_note=phys_note
            )
            db.session.add(new_medication)
        db.session.commit()
        return redirect(url_for('main.physicianPatientDetails', patient_id=patient_id))
    print('something went wrong...')
    return redirect(url_for('main.index'))

# chat
@socketio.on('send_message')
def send_message(data):
    chat = Chats(patient_id=data['patient_id'], physician_id=data['physician_id'], content=data['message_content'], sent_by=data['sent_by'])
    db.session.add(chat)
    db.session.commit()

    # emit the new message to the physician's room
    socketio.emit('receive_message', data, room=data['physician_id'])

@main.route('/get_chat_history')
@protected_route
def get_chat_history():
    physician_id = request.args.get('physician_id')
    patient_id = request.args.get('patient_id')
    chats = Chats.query.filter(and_(Chats.patient_id==patient_id, Chats.physician_id==physician_id)).all() 
    messages = [{"content": chat.content, "sent_by": chat.sent_by, "sent": chat.sent, "is_read": chat.is_read} for chat in chats]
    return jsonify(messages=messages)

# update a refill status when a patient
def update_chat(physician_id, patient_id, message, sent_by):
    try:
        new_chat = Chats(physician_id=physician_id, patient_id=patient_id, content=message, sent_by=sent_by)
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({"success": "Message was successfully uploaded"}), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

# API ENDPOINTS
@main.route('/')
def index():
    if 'usertype' in session:
        if session['usertype'] == 'patient':
            return redirect(f'/patient?patient_id={current_user.id}')
        elif session['usertype'] == 'physician':
            return redirect(f'/physician?physician_id={current_user.id}')
        elif session['usertype'] == 'pharmacy':
            return redirect(f'/pharmacy?pharmacy_id={current_user.id}')
    return render_template('index.html')

@main.route('/physician/')
@main.route('/physician')
@protected_route
@physician_protected_route
def physician(page=1):
    physician_id = current_user.id
    page = request.args.get('page')
    if(page == None):
        page = 1
    response, status_code = get_calendar_physician(physician_id)
    if status_code == 200:
        appointments = response.get_json()
        response2, status_code2 = get_physicians_patients(physician_id)
        if status_code2 == 200:
            patients = response2.get_json()
            return render_template('users/physician.html', page=page, appointments=appointments, patients=patients, physician_id=physician_id)
        else:
            error_message = "An error occurred while retrieving patients."
            return error_message, 500
    else:
        error_message = "An error occurred while retrieving appointments."
        return error_message, 500

# URL handling for physician page
@main.route('/physician/<path:trailing>')
@protected_route
@physician_protected_route
def physician_manual(trailing=''):  # manually set url
    if trailing != '':
        pattern = re.compile(r'page=(\d+)')
        result = pattern.search(trailing)
        if result:
            page = result.group(1)
            return redirect(url_for('main.physician', page=page))
    return redirect(url_for('main.physician', page=1))

# default pharmacy page
@main.route('/pharmacy/')
@main.route('/pharmacy')
@protected_route
@pharmacy_protected_route
def pharmacy(page=1):
    page = request.args.get('page')
    if(page == None):
        page = 1
    return render_template('users/pharmacist.html', page=page)

# URL handling for pharmacy page
@main.route('/pharmacy/<path:trailing>')
@protected_route
@pharmacy_protected_route
def pharmacy_manual(trailing=''):  # manually set url
    if trailing != '':
        pattern = re.compile(r'page=(\d+)')
        result = pattern.search(trailing)
        if result:
            page = result.group(1)
            return redirect(url_for('main.pharmacy', page=page))
    return redirect(url_for('main.pharmacy', page=1))

@main.route('/pharmacyPatientDetails', methods=['POST','GET'])
@pharmacy_protected_route
@protected_route
def pharmacyPatientDetails():
    patient_id = request.args.get('patient_id')
    if patient_id == None:
        return redirect(url_for("index"))
    else:
        response, status_code = get_patient_medications(patient_id)
        if status_code == 200:
            patient_meds = response.get_json()
            response2, status_code2 = get_patient_info(patient_id)
            if status_code2 == 200:
                data = response2.get_json()
                patient_info = data.get("patient_info")
                patient_pharmacy = data.get("pharmacy")
                return render_template('users/pharmacyPatientDetails.html', patient_meds=patient_meds, patient_info=patient_info, patient_pharmacy=patient_pharmacy, patient_id=patient_id)
            else:
                error_message = "An error occurred while retrieving patient info."
                return error_message, 500
        else:
            error_message = "An error occurred while retrieving patient medications."
            return error_message, 500
        

@main.route('/pharmacistAutoRefill', methods=['POST','GET'])
@pharmacy_protected_route
@protected_route
def pharmacistAutoRefill():
    response, status_code = get_patient_refills()
    if status_code == 200:
        refills = response.get_json()
        return render_template('users/pharmacistAutoRefill.html', refills=refills)
    else:
        error_message = "An error occurred while retrieving patient refill information."
        return error_message, 500

@main.route('/update_refill_status', methods=['POST'])
@pharmacy_protected_route
@protected_route
def update_refill_status():
    data = request.get_json()
    pat_med_pharId = data['pat_med_pharId']
    print(pat_med_pharId)
    patient_id, med_id, pharmacy_id = pat_med_pharId.split()
    try:
        response, status_code = update_refill(patient_id, med_id, pharmacy_id)   
        if status_code==200:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'Update failed'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# helper function for physician and pharmacy page
@main.route('/searchResult', methods=['POST','GET'])
@protected_route
def search_result():
    results = {}
    if request.method == 'POST':
        search_word = request.form.get('query')
        if search_word:
            # Queries for first 20 patients that fit the search word in related columns
            patients = db.session.query(Patient).filter(
                # Combines multiple filter conditions with logical OR operator
                or_(
                    Patient.first_name.startswith(f"{search_word}"),
                    Patient.last_name.startswith(f"{search_word}"),
                    Patient.id.startswith(f"{search_word}"),
                    Patient.city.startswith(f"{search_word}"),
                )
            ).order_by(Patient.id.desc()).limit(20).all()
        else:
            patients = Patient.query.all()
    for patient in patients:
        result = {
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "city": patient.city
        }
        results[str(patient.id)] = result
    return jsonify(results)

# maps.html
@main.route('/maps', methods=['POST','GET'])
@protected_route
def maps():
    patient_id = request.args.get('id')
    response, status_code = get_coordinates_spec(patient_id)
    # check if status code is OK
    if status_code == 200:
        # extract JSON data from response
        center_coords = response.get_json()
        response2, status_code2 = get_coordinates_all()
        if status_code2 == 200:
            all_coords = response2.get_json()
            print('ogay')
            return render_template('maps.html', coordinates=center_coords, all_coords=all_coords, patient_id=patient_id)
        else:
            error_message = "An error occurred while retrieving all coordinates."
            return error_message, 500
    else:
        error_message = "An error occurred while retrieving specific coordinates."
        return error_message, 500
    
@main.route('/change-pharmacy', methods=['POST'])
@protected_route
def change_primary_pharmacy():
    patient_id = request.args.get('patient_id')
    new_pharmacy_id = request.args.get('pharmacy_id')
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:
            patient.pharmacy_id = new_pharmacy_id  # Update the pharmacy_id
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# maps_nonpatient.html
@main.route('/maps_nonpatient', methods=['POST','GET'])
@protected_route
def maps_nonpatient():
    patient_id = request.args.get('id')
    response, status_code = get_coordinates_spec(patient_id)
    # check if status code is OK
    if status_code == 200:
        # extract JSON data from response
        center_coords = response.get_json()
        response2, status_code2 = get_coordinates_all()
        if status_code2 == 200:
            all_coords = response2.get_json()
            return render_template('maps_nonpatient.html', coordinates=center_coords, all_coords=all_coords, patient_id=patient_id)
        else:
            error_message = "An error occurred while retrieving all coordinates."
            return error_message, 500
    else:
        error_message = "An error occurred while retrieving specific coordinates."
        return error_message, 500

# patient.html
@main.route('/patient', methods=['POST', 'GET'])
@protected_route
@patient_protected_route
def patient():
    patient_id = request.args.get('patient_id')
    response, status_code = get_patient_medications(patient_id)
    if status_code == 200:
        patient_meds = response.get_json()
        response2, status_code2 = get_patient_info(patient_id)
        if status_code2 == 200:
            data = response2.get_json()
            patient_info = data.get("patient_info")
            patient_pharmacy = data.get("pharmacy")
            response3, status_code3 = get_alerts(patient_id)
            if status_code3 == 200:
                alerts = response3.get_json()
                response4, status_code4 = get_patients_physicians(patient_id)
                if status_code4 == 200:
                    physicians = response4.get_json()
                    response5, status_code5 = get_calendar_patient(patient_id, physicians)
                    if status_code5 == 200:
                        appointments = response5.get_json()
                        return render_template('users/patient.html', patient_meds=patient_meds, patient_info=patient_info, patient_pharmacy=patient_pharmacy, patient_id=patient_id,
                                           alerts=alerts, physicians=physicians, appointments=appointments)
                    else:
                        error_message = "An error occurred while retrieving appointments."
                        return error_message, 500
                else:
                    error_message = "An error occurred while retrieving associated physicians."
                    return error_message, 500   
            else:
                error_message = "An error occurred while retrieving medication alerts."
                return error_message, 500
        else:
            error_message = "An error occurred while retrieving patient info."
            return error_message, 500
    else:
        error_message = "An error occurred while retrieving patient medications."
        return error_message, 500    

@main.route('/request_appointment', methods=['POST'])
@protected_route
def request_appointment():
    data = request.get_json()
    id = data.get('id')
    patient_id = data.get('patient_id')
    try:
        entry = Availability.query.filter_by(id=id).first()
        entry.status = 'requested'
        entry.patient_id = patient_id
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main.route('/cancel_appointment', methods=['POST', 'GET'])
@protected_route
def cancel_appointment():
    data = request.get_json()
    id = data.get('id')
    try:
        entry = Availability.query.filter_by(id=id).first()
        entry.status = 'available'
        entry.patient_id = None
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main.route('/approve_appointment', methods=['POST', 'GET'])
@protected_route
def approve_appointment():
    data = request.get_json()
    id = data.get('id')
    try:
        entry = Availability.query.filter_by(id=id).first()
        entry.status = 'appointment'
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@main.route('/delete_appointment', methods=['POST', 'GET'])
@protected_route
def delete_appointment():
    data = request.get_json()
    id = data.get('id')
    try:
        entry = Availability.query.filter_by(id=id).first()
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main.route('/update_chat_history', methods=['POST'])
@protected_route
def update_chat_history():
    data = request.get_json()
    physician_id = data['physician_id']
    patient_id = data['patient_id']
    message = data['message']
    sent_by = data['sent_by']
    try:
        response, status_code = update_chat(physician_id, patient_id, message, sent_by)
        if status_code==200:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'Update failed'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@main.route('/uploads/<filename>')
@protected_route
def get_file(filename):
    return send_from_directory(main.config['UPLOAD_FOLDER'], filename)

@main.route('/patient_info', methods=['POST','GET'])
@protected_route
def patient_info():
    fernet = Fernet(os.getenv('ENCRYPTION_KEY').encode())
    upload_form = UploadForm()
    edit_form = EditButtonForm()
    version = 1
    decrypted_url = ''
    patient_id = request.args.get('id')
    response, status_code = get_patient_info(patient_id)
    if status_code == 200:
        data = response.get_json()
        patient_info = data.get("patient_info")
        patient_allergies = data.get("allergies")
        patient_diseases = data.get("diseases")
        response2, status_code2 = get_alerts(patient_id)
        if status_code2 == 200:
            alerts = response2.get_json()
            encrypted_url = patient_info[0]['insurance_url']
            if encrypted_url:
                decrypted_url = fernet.decrypt(encrypted_url.encode()).decode()
                if decrypted_url[60:70] == str(date.today()):
                    _, version = decrypted_url.rsplit('v')
                    version = int(version) + 1            
            if upload_form.validate_on_submit():
                patient = Patient.query.filter_by(id=patient_id).first()
                if upload_form.file:
                    filename = secure_filename(upload_form.file.data.filename)
                    if allowed_file(filename):
                        # Add insurance card to uploads folder
                        upload_form.file.data.save(f'uploads/{filename}')
                        file_url = upload_to_bucket(f'Insurance_Uploads/{patient.username}_{date.today()}_v{version}',
                                                    f'uploads/{filename}', os.getenv('BUCKET_NAME')).encode()
                        encrypted_url = fernet.encrypt(file_url).decode()
                        patient.insurance_url = encrypted_url
                        db.session.commit()
                return redirect(url_for('main.patient_info', id=patient_id))
            if edit_form.validate_on_submit():
                return redirect(url_for('main.edit_patient_info', id=patient_id))
            return render_template('users/patientInfo.html', patient_info=patient_info, patient_allergies=patient_allergies,
                                patient_diseases=patient_diseases, patient_id=patient_id, file_url=decrypted_url,
                                upload_form=upload_form, edit_form=edit_form, alerts=alerts)
        else:
            error_message = "An error occured while retriving alerts."
            return error_message, 500
    else:
        error_message = "An error occurred while retrieving patient info."
        return error_message, 500
    
@main.route('/patientInfo_nonpatient', methods=['POST','GET'])
@protected_route
def patientInfo_nonpatient():
    version = 1
    patient_id = request.args.get('id')
    response, status_code = get_patient_info(patient_id)
    if status_code == 200:
        data = response.get_json()
        patient_info = data.get("patient_info")
        patient_allergies = data.get("allergies")
        patient_diseases = data.get("diseases")

        file_url = patient_info[0]['insurance_url']
        if file_url:
            if file_url[60:70] == str(date.today()):
                _, version = file_url.rsplit('v')
                version = int(version) + 1
        return render_template('users/patientInfo_nonpatient.html', patient_info=patient_info, patient_allergies=patient_allergies,
                               patient_diseases=patient_diseases, patient_id=patient_id, file_url=file_url, usertype=session['usertype'])
    else:
        error_message = "An error occurred while retrieving patient info."
        return error_message, 500

@main.route('/edit_patient_info', methods=['POST','GET'])
@protected_route
def edit_patient_info():
    patient_id = request.args.get('id')
    response, status_code = get_patient_info(patient_id)
    if status_code == 200:
        data = response.get_json()
        patient_info = data.get("patient_info")
        patient_allergies = data.get("allergies")
        patient_diseases = data.get("diseases")

        form = EditInfoForm(first_name = patient_info[0]['first_name'],
                            last_name = patient_info[0]['last_name'],
                            d_o_b = datetime.strptime(patient_info[0]['d_o_b'], '%Y-%m-%d').date(),
                            sex = patient_info[0]['sex'],
                            phone_number = patient_info[0]['phone_number'],
                            emergency_cont = patient_info[0]['emergency_cont'],
                            building_num = patient_info[0]['building_num'],
                            apt_num = patient_info[0]['apt_num'],
                            street_name = patient_info[0]['street_name'],
                            city = patient_info[0]['city'],
                            state = patient_info[0]['state'],
                            zip_code = patient_info[0]['zip_code'],)
        back_form = BackForm()

        if back_form.validate_on_submit():
            return redirect(url_for('main.patient_info', id=patient_id))

        if form.validate_on_submit():
            patient = Patient.query.filter_by(id=patient_id).first()
            patient.first_name = form.first_name.data
            patient.last_name = form.last_name.data
            patient.d_o_b = form.d_o_b.data
            patient.sex = form.sex.data
            patient.phone_number = form.phone_number.data
            patient.emergency_cont = form.emergency_cont.data
            patient.building_num = form.building_num.data
            patient.apt_num = form.apt_num.data
            patient.street_name = form.street_name.data
            patient.city = form.city.data
            patient.state = form.state.data
            patient.zip_code = form.zip_code.data
            db.session.commit()
            flash('You have successfully editted your profile!')
            return redirect(url_for('main.patient_info', id=patient_id))
        
        return render_template('users/editPatientInfo.html', patient_id=patient_id, patient_allergies=patient_allergies,
                               patient_diseases=patient_diseases, form=form, back_form=back_form)
    else:
        error_message = "An error occurred while retrieving patient info."
        return error_message, 500

# if __name__ == '__main__':
#     # set FLASK_APP=main.py
#     # flask run
#     main.run(debug=True)

# source venv/bin/activate
# lsof -i :5000
# kill -9 PID
# mysql -u root -p
# USE mediconnect_db;
# git status -> which branch you're working on
# git branch "name" -> creates new branch
# git branch -l -> shows all branches
# git checkout "name" -> switches to branch
# git push --set-upstream origin "name" -> set upstream branch for branch
# git pull origin "name" -> pulls someone else's branch to your computer
# git add . -> mount files to be committed
# git commit -m "" -> commmit changes to branch with message
# git push origin "name" -> pushes commits and changes to github branch

# BEFORE PUSHING, ADD PASSWORD DATABASE URI