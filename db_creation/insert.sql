INSERT INTO Pharmacy(username, password, pharmacy_name, email, building_num, street_name, city, state, zip_code, coord, phone_number) VALUES ('DR', '1234', 'Duane Reade', 'duanereade@example.com', '386', 'Fulton St', 'Brooklyn', 'NY', 11201, ST_GeogFromText('SRID=4326;POINT(-73.98723322800296 40.691331310921875)'), '(718) 330-0363'), 
('CVS', '1234', 'CVS Pharmacy', 'cvs@example.com','217', 'Broadway', 'New York', 'NY', 10007, ST_GeogFromText('SRID=4326;POINT(-74.0086964544864 40.711878583096414)'), '(212) 331-7895'),
('Walgreens', '1234', 'Walgreens', 'walgreens@example.com', '120', 'Court St', 'Brooklyn', 'NY', 11201, ST_GeogFromText('SRID=4326;POINT(-73.99261230709112 40.69150908529599)'), '(718) 643-2146'),
('BHS', '1234', 'Brooklyn Hospital Center', 'bhs@example.com', '86', 'Fleet Pl', 'Brooklyn', 'NY', 11201, ST_GeogFromText('SRID=4326;POINT(-73.98193649056897 40.695111885907956)'), '(718) 250-7998'),
('LC', '1234', 'Liberty Chemists', 'giancab.retail@gmail.com', '1501', 'Newkirk Avenue', 'Brooklyn', 'NY', 11226, ST_GeogFromText('SRID=4326;POINT(-73.9632823355658 40.636433829508185)'), '(718) 676-5995');
 
INSERT INTO Hospital(hospital_name, building_num, street_name, city, state, zip_code, coord, phone_number) VALUES ('Mount Sinai Medical Center', '300', 'Cadman Plz W', 'Brooklyn', 'NY', 11201, ST_GeogFromText('SRID=4326;POINT(-73.991819046455 40.70042412470124)'), '(929) 210-6000'),
('The Brooklyn Hospital Center', '121', 'Dekalb Ave', 'Brooklyn', 'NY', 11201, ST_GeogFromText('SRID=4326;POINT(-73.97944296941733 40.69531888856064)'), '(718) 250-8000'),
('New York Presbyterian Brooklyn Methodist Hospital', '536', '5th St', 'Brooklyn', 'NY', 11215, ST_GeogFromText('SRID=4326;POINT(-73.97824771667521 40.67249032164987)'), '(718) 943-4343'),
('NYC Health + Hospitals/Bellevue', '426', '1st Ave', 'New York', 'NY', 10016, ST_GeogFromText('SRID=4326;POINT(-73.97637945249116 40.741608144919944)'), '(212) 562-5555'),
('Presbyterian Lower Manhattan Hospital', '170', 'William St', 'New York', 'NY', 10038, ST_GeogFromText('SRID=4326;POINT(-74.00562137678385 40.71465459704797)'), '(212) 312-5000');

INSERT INTO Physician(username, password, first_name, last_name, email, phone_number, hospital_id) VALUES ('RM', '1234', 'Ryan', 'Mire', 'ryanmire@example.com', '(212) 345-6789', 1),
('AG', '1234', 'Alec', 'Goldenberg', 'alexgoldenberg@example.com', '(646) 789-0123', 2),
('MF', '1234', 'Mike', 'Feinstein', 'mikefeinstein@example.com', '(917) 456-7890', 3),
('CC', '1234', 'Chanel', 'Coble', 'chanelcoble@example.com', '(347) 123-4567', 4),
('SC', '1234', 'Sandra', 'Curit', 'giancab.finance@gmail.com', '(929) 987-6543', 5);

INSERT INTO Patient(username, password, first_name, last_name, d_o_b, sex, email, phone_number, emergency_cont, building_num, street_name, apt_num, city, state, zip_code, pharmacy_id) VALUES
('NR', '1234', 'Nisha', 'Ramanna', '2002-05-17', 'Female', 'nramanna@eg.poly.edu', '(615) 788-4556', 'Sujatha Ramanna', '11', 'Hoyt St', '29G', 'Brooklyn', 'NY', 11201, 200000),
('GC', '1234', 'Giancarlos', 'Cabrera', '2001-11-25', 'Male', 'giancab25@gmail.com', '(631) 332-3800', 'Tania Cortes Alonso', '200', 'East 6th St', '4A', 'New York', 'NY', 10003, 200000),
('SP', '1234', 'Sofia', 'Papathanasiou', '2004-04-23', 'Female', 'spapathanasiou@eg.poly.edu', '(518) 253-6785', 'Mirna Ashour', '636', 'Greenwich St', '5J', 'Manhattan', 'NY', 10014, 200000),
('MA', '1234', 'Mirna', 'Ashour', '2002-11-20', 'Female', 'mashour@eg.poly.edu', '(347) 320-2799', 'Sofia Papathanasiou', '152', 'Montague', '2V', 'Brooklyn', 'NY', 11201, 200000),
('TP', '1234', 'Teddy', 'Polkosnik', '2003-04-05', 'Male', 'tpolkosnik@eg.poly.edu', '(516) 444-0718', 'Leon Polkosnik', '30', 'Sprague Dr', '4C', 'Valley Stream', 'NY', 11580, 200000),
('JD', '1234', 'John', 'Doe', '1990-01-01', 'Male', 'johndoe@example.com', '(555) 111-2222', 'Jane Doe', '100', 'Main St', '1A', 'New York', 'NY', 10001, 200000),
('ES', '1234', 'Emily', 'Smith', '1992-02-02', 'Female', 'emilysmith@example.com', '(555) 333-4444', 'Evan Smith', '200', 'Lake Ave', '2B', 'Brooklyn', 'NY', 10002, 200000),
('MJ', '1234', 'Michael', 'Johnson', '1988-03-03', 'Male', 'michaeljohnson@example.com', '(555) 555-6666', 'Michelle Johnson', '300', 'Park Blvd', '3C', 'Queens', 'NY', 10003, 200000),
('AW', '1234', 'Alice', 'Wong', '1993-04-04', 'Female', 'alicewong@example.com', '(555) 777-8888', 'Aaron Wong', '400', 'Broadway', '4D', 'Manhattan', 'NY', 10004, 200001),
('RM', '1234', 'Robert', 'Miller', '1985-05-05', 'Male', 'robertmiller@example.com', '(555) 999-0000', 'Rachel Miller', '500', 'Fifth Ave', '5E', 'Bronx', 'NY', 10005, 200001),
('LB', '1234', 'Linda', 'Brown', '1991-06-06', 'Female', 'lindabrown@example.com', '(555) 010-2020', 'Logan Brown', '600', 'Madison Ave', '6F', 'Staten Island', 'NY', 10006, 200001),
('DG', '1234', 'Daniel', 'Garcia', '1989-07-07', 'Male', 'danielgarcia@example.com', '(555) 303-4040', 'Diana Garcia', '700', 'Lexington Ave', '7G', 'New York', 'NY', 10007, 200001),
('SM', '1234', 'Sarah', 'Martinez', '1987-08-08', 'Female', 'sarahmartinez@example.com', '(555) 505-6060', 'Simon Martinez', '800', 'Wall St', '8H', 'Brooklyn', 'NY', 10008, 200001),
('BL', '1234', 'Brian', 'Lee', '1994-09-09', 'Male', 'brianlee@example.com', '(555) 707-8080', 'Brenda Lee', '900', 'Prince St', '9I', 'Queens', 'NY', 10009, 200001),
('NA', '1234', 'Nancy', 'Anderson', '1986-10-10', 'Female', 'nancyanderson@example.com', '(555) 909-1010', 'Neil Anderson', '1000', 'King St', '10J', 'Manhattan', 'NY', 10010, 200001),
('JT', '1234', 'Julia', 'Thomas', '1995-11-11', 'Female', 'juliathomas@example.com', '(555) 111-1212', 'Jack Thomas', '1100', 'Queen St', '11K', 'Bronx', 'NY', 10011, 200002),
('SH', '1234', 'Steven', 'Harris', '1984-12-12', 'Male', 'stevenharris@example.com', '(555) 131-1414', 'Susan Harris', '1200', 'Duke St', '12L', 'Staten Island', 'NY', 10012, 200002),
('AM', '1234', 'Angela', 'Martinez', '1993-01-13', 'Female', 'angelamartinez@example.com', '(555) 151-1616', 'Anthony Martinez', '1300', 'Earl St', '13M', 'Brooklyn', 'NY', 10013, 200002),
('GW', '1234', 'Gregory', 'Wilson', '1992-02-14', 'Male', 'gregorywilson@example.com', '(555) 171-1818', 'Grace Wilson', '1400', 'Baron St', '14N', 'New York', 'NY', 10014, 200002),
('DT', '1234', 'Dorothy', 'Taylor', '1991-03-15', 'Female', 'dorothytaylor@example.com', '(555) 191-2021', 'Dylan Taylor', '1500', 'Count St', '15O', 'Queens', 'NY', 10015, 200002),
('OJ', '1234', 'Olivia', 'Jackson', '1988-04-16', 'Female', 'oliviajackson@example.com', '(555) 212-2223', 'Owen Jackson', '1600', 'Marquis St', '16P', 'Manhattan', 'NY', 10016, 200002),
('EM', '1234', 'Ethan', 'Moore', '1987-05-17', 'Male', 'ethanmoore@example.com', '(555) 232-2425', 'Eva Moore', '1700', 'Viscount St', '17Q', 'Bronx', 'NY', 10017, 200002),
('SC', '1234', 'Sophia', 'Clark', '1989-06-18', 'Female', 'sophiaclark@example.com', '(555) 252-2627', 'Samuel Clark', '1800', 'Knight St', '18R', 'Staten Island', 'NY', 10018, 200002),
('LR', '1234', 'Lucas', 'Rodriguez', '1990-07-19', 'Male', 'lucasrodriguez@example.com', '(555) 272-2829', 'Lily Rodriguez', '1900', 'Dame St', '19S', 'Brooklyn', 'NY', 10019, 200002),
('ML', '1234', 'Mia', 'Lewis', '1992-08-20', 'Female', 'mialewis@example.com', '(555) 292-3031', 'Mason Lewis', '2000', 'Earl St', '20T', 'New York', 'NY', 10020, 200003),
('IM', '1234', 'Isabella', 'Martinez', '1993-09-21', 'Female', 'isabellamartinez@example.com', '(555) 313-3233', 'Ian Martinez', '2100', 'Countess St', '21U', 'Queens', 'NY', 10021, 200003),
('NB', '1234', 'Noah', 'Brown', '1986-10-22', 'Male', 'noahbrown@example.com', '(555) 333-3435', 'Natalie Brown', '2200', 'Duchess St', '22V', 'Manhattan', 'NY', 10022, 200003),
('EG', '1234', 'Emma', 'Garcia', '1984-11-23', 'Female', 'emmagarcia@example.com', '(555) 353-3637', 'Evan Garcia', '2300', 'Baroness St', '23W', 'Bronx', 'NY', 10023, 200003),
('WJ', '1234', 'William', 'Jones', '1995-12-24', 'Male', 'williamjones@example.com', '(555) 373-3839', 'Wendy Jones', '2400', 'Count St', '24X', 'Staten Island', 'NY', 10024, 200003),
('AL', '1234', 'Ava', 'Lee', '1991-01-25', 'Female', 'avalee@example.com', '(555) 393-4041', 'Aaron Lee', '2500', 'Viscount St', '25Y', 'Brooklyn', 'NY', 10025, 200003),
('JW', '1234', 'James', 'Wilson', '1987-02-26', 'Male', 'jameswilson@example.com', '(555) 413-4243', 'Julia Wilson', '2600', 'Marquess St', '26Z', 'New York', 'NY', 10026, 200003),
('SD', '1234', 'Sophie', 'Davis', '1989-03-27', 'Female', 'sophiedavis@example.com', '(555) 433-4445', 'Scott Davis', '2700', 'Knight St', '27AA', 'Queens', 'NY', 10027, 200003),
('BM', '1234', 'Benjamin', 'Miller', '1990-04-28', 'Male', 'benjaminmiller@example.com', '(555) 453-4647', 'Bethany Miller', '2800', 'Squire St', '28BB', 'Manhattan', 'NY', 10028, 200004),
('CA', '1234', 'Charlotte', 'Anderson', '1992-05-29', 'Female', 'charlotteanderson@example.com', '(555) 473-4849', 'Charles Anderson', '2900', 'Lady St', '29CC', 'Bronx', 'NY', 10029, 200004),
('ET', '1234', 'Elijah', 'Taylor', '1993-06-30', 'Male', 'elijahtaylor@example.com', '(555) 493-5051', 'Ella Taylor', '3000', 'Lord St', '30DD', 'Staten Island', 'NY', 10030, 200004),
('AH', '1234', 'Amelia', 'Harris', '1994-07-31', 'Female', 'ameliaharris@example.com', '(555) 513-5253', 'Adam Harris', '3100', 'Duke St', '31EE', 'Brooklyn', 'NY', 10031, 200004),
('LC', '1234', 'Logan', 'Clark', '1988-08-01', 'Male', 'loganclark@example.com', '(555) 533-5455', 'Linda Clark', '3200', 'Prince St', '32FF', 'New York', 'NY', 10032, 200004),
('HR', '1234', 'Harper', 'Rodriguez', '1985-09-02', 'Female', 'harperrodriguez@example.com', '(555) 553-5657', 'Henry Rodriguez', '3300', 'King St', '33GG', 'Queens', 'NY', 10033, 200004),
('LL', '1234', 'Lucas', 'Lopez', '1996-10-03', 'Male', 'lucaslopez@example.com', '(555) 573-5859', 'Luna Lopez', '3400', 'Queen St', '34HH', 'Manhattan', 'NY', 10034, 200004),
('MG', '1234', 'Mia', 'Gonzalez', '1997-11-04', 'Female', 'miagonzalez@example.com', '(555) 593-6061', 'Marco Gonzalez', '3500', 'Duchess St', '35II', 'Bronx', 'NY', 10035, 200004),
('AC', '1234', 'Aiden', 'Cal', '1998-12-05', 'Male', 'aidencal@example.com', '(555) 613-6263', 'Avery Wilson', '3600', 'Baroness St', '36JJ', 'Staten Island', 'NY', 10036, 200004);

INSERT INTO Patient_allergies VALUES (100000, 'Peanuts'), (100000, 'Peaches'), (100000, 'Dogs'), (100000, 'Penicillin');

INSERT INTO Medication(medication_name, side_effects) VALUES ('Lexapro', 'Decreased appetite, Nausea, Trouble sleeping, Confusion'), ('Lipitor', 'Joint pain, Muscle stiffness, Chest pain'), ('Zestril', 'Blurred vision, Dizziness, Rash');
INSERT INTO Medication(medication_name, side_effects, instruction_vid_name, instruction_vid_url) VALUES ('Asthma Inhaler', 'Cough, Horseness, Palpitations', 'How to Use an Asthma Inhaler', 'https://storage.cloud.google.com/sql4523/How%20to%20Use%20an%20Inhaler.mp4');
INSERT INTO Medication(medication_name, side_effects) VALUES ('Gabapentin', 'Swollen limbs, Dizziness');

INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100000, 1, 'Lexapro', '100mg', 'Daily', 30, '2025-02-22', 300000, '2024-02-22', 'If this drug affects your sleep, please take 30mg of melatonin at night.');
INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100000, 2, 'Lipitor', '20mg', '2x Daily', 90, '2025-01-01', 300000, '2024-01-01', 'Please remember to take Lipitor at the same time each day, and note that you might experience mild muscle pain, which is a common side effect; however, contact me if you experience severe muscle pain or weakness.');
INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100000, 3, 'Zestril', '50mg', 'Daily', 30, '2024-09-18', 300000, '2023-09-18', 'Be cautious about possible dizziness during the first few days on Zestril, especially when standing up quickly, as this medication can lower your blood pressure significantly.');
INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100000, 4, 'Asthma Inhaler', 'N/A', 'As needed', 365, '2025-04-10', 300002, '2024-04-10', 'Use your asthma inhaler as directed, typically one or two puffs to relieve asthma symptoms; always carry it with you in case of sudden asthma attacks, and rinse your mouth after use to prevent irritation.');
INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100000, 5, 'Gabapentin', '40mg', 'Weekly', 30, '2024-04-10', 300002, '2023-04-10', 'None');

INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100001, 1, 'Lexapro', '100mg', 'Daily', 30, '2025-02-22', 300000, '2024-02-22', 'If this drug affects your sleep, please take 30mg of melatonin at night.');
INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100001, 2, 'Lipitor', '20mg', '2x Daily', 90, '2025-01-01', 300002, '2024-01-01', 'Please remember to take Lipitor at the same time each day, and note that you might experience mild muscle pain, which is a common side effect; however, contact me if you experience severe muscle pain or weakness.');
INSERT INTO Patient_medications(patient_id, medication_id, medication_name, dosage, frequency, days_supply, prescription_valid_till, physician_id, date_prescribed, phys_note) VALUES (100001, 3, 'Zestril', '50mg', 'Daily', 30, '2024-09-18', 300003, '2023-09-18', 'Be cautious about possible dizziness during the first few days on Zestril, especially when standing up quickly, as this medication can lower your blood pressure significantly.');

INSERT INTO Patient_diseases VALUES (100000, 'Asthma'), (100000, 'Diabetes'), (100000, 'ADHD'), (100000, 'Arthritis');

INSERT INTO Availability(available_date, available_time, status, physician_id) VALUES ('2024-05-01', '12:30:00', 'appointment', 300000), ('2024-05-07', '15:45:00', 'requested', 300000), ('2024-05-10', '03:00:00', 'appointment', 300000)
