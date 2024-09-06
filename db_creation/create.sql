CREATE TABLE Pharmacy (
    id SERIAL,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    pharmacy_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    building_num int NOT NULL,
	street_name varchar(255) NOT NULL,
	apt_num varchar(255),
	city varchar(255) NOT NULL,
	state varchar(255) NOT NULL,
	zip_code int NOT NULL,
    -- longitude latitude
    -- coord point NOT NULL,
    coord GEOGRAPHY(POINT, 4326) NOT NULL,
    phone_number varchar(255) NOT NULL,
    PRIMARY KEY (id)
);
-- ALTER TABLE Pharmacy AUTO_INCREMENT=200000;
SELECT setval(pg_get_serial_sequence('Pharmacy', 'id'), 200000, false);

CREATE TABLE Hospital (
    id SERIAL,
    hospital_name varchar(255) NOT NULL,
    building_num int NOT NULL,
	street_name varchar(255) NOT NULL,
	apt_num varchar(255),
	city varchar(255) NOT NULL,
	state varchar(255) NOT NULL,
	zip_code int NOT NULL,
    -- coord point NOT NULL,
    coord GEOGRAPHY(POINT, 4326) NOT NULL,
    phone_number varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Physician (
    id SERIAL,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    phone_number varchar(255) NOT NULL,
    hospital_id int NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES Hospital(id),
    PRIMARY KEY(id)
);
-- ALTER TABLE Physician AUTO_INCREMENT=300000;
SELECT setval(pg_get_serial_sequence('Physician', 'id'), 300000, false);

CREATE TABLE Patient (
    id SERIAL,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    d_o_b date NOT NULL,
    sex varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    phone_number varchar(255) NOT NULL,
    emergency_cont varchar(255) NOT NULL,
    building_num int NOT NULL,
	street_name varchar(255) NOT NULL,
	apt_num varchar(255),
	city varchar(255) NOT NULL,
	state varchar(255) NOT NULL,
	zip_code int NOT NULL,
    pharmacy_id int NOT NULL,
    insurance_url varchar(510),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(id),
    PRIMARY KEY (id)
);
-- ALTER TABLE Patient AUTO_INCREMENT=100000;
SELECT setval(pg_get_serial_sequence('Patient', 'id'), 100000, false);

-- id -> patient_id
CREATE TABLE Patient_allergies (
    patient_id int,
    allergy_name varchar(255),
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    PRIMARY KEY(patient_id, allergy_name)
);

-- id -> patient_id
CREATE TABLE Patient_diseases (
    patient_id int,
    disease_name varchar(255),
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    PRIMARY KEY(patient_id, disease_name)
);


CREATE TABLE Medication (
    id SERIAL,
    medication_name varchar(255) NOT NULL,
    side_effects varchar(510) NOT NULL,
    instruction_vid_name varchar(255),
    instruction_vid_url varchar(510),
    PRIMARY KEY (id)
);

-- edit
-- id -> patient_id
-- medication_id added, medication_name eventually removed
CREATE TABLE Patient_medications (
    patient_id int,
    medication_id int NOT NULL,
    medication_name varchar(255) NOT NULL,
    dosage varchar(255) NOT NULL,
    frequency varchar(255) NOT NULL,
    days_supply int NOT NULL,
    prescription_valid_till date NOT NULL,
    physician_id int NOT NULL,
    date_prescribed date NOT NULL,
    next_refill_date date,
    phys_note varchar(510),
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (medication_id) REFERENCES Medication(id),
    FOREIGN KEY (physician_id) REFERENCES Physician(id),
    PRIMARY KEY(patient_id, medication_id)
);

CREATE TABLE Refill_notifications (
    id SERIAL,
    patient_id int NOT NULL,
    medication_id int NOT NULL,
    pharmacy_id int NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (medication_id) REFERENCES Medication(id),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(id),
    PRIMARY KEY(id)
);

-- id -> patient_id
-- medication_id added, medication_name eventually removed
CREATE TABLE Medication_notes (
    patient_id int,
    medication_id int,
    physician_id int,
    notes varchar(510) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (medication_id) REFERENCES Medication(id),
    FOREIGN KEY (physician_id) REFERENCES Physician(id),
    PRIMARY KEY(patient_id, medication_id, physician_id)
);

CREATE TABLE Treats (
    physician_id int,
    patient_id int,
    FOREIGN KEY (physician_id) REFERENCES Physician(id),
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    PRIMARY KEY (physician_id, patient_id)
);

-- medication_id added, medication_name eventually removed
CREATE TABLE Pharmacy_auto_refills (
    pharmacy_id int,
    patient_id int,
    medication_id int,
    medication_name varchar(255),
    is_complete BOOLEAN NOT NULL,
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(id),
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (medication_id) REFERENCES Medication(id),
    PRIMARY KEY (pharmacy_id, patient_id, medication_id)
);

CREATE TABLE Chats (
    id SERIAL,
    patient_id int NOT NULL,
    physician_id int NOT NULL,
    content TEXT NOT NULL,
    sent_by varchar(255) NOT NULL,
    sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (physician_id) REFERENCES Physician(id),
    PRIMARY KEY (id)
);

CREATE TABLE Availability (
    id SERIAL,
    available_date DATE NOT NULL,
    available_time TIME NOT NULL,
    status varchar(255) NOT NULL,
    physician_id int NOT NULL,
    patient_id int,
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (physician_id) REFERENCES Physician(id),
    PRIMARY KEY (id)
);