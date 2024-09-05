############################## helper functions ##############################
def random_string(size:int=10) -> str:
    import string, random
    result = ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))
    return result

def check_usertype(client, url:str='/', usertype=None, status=200) -> None:
    with client.session_transaction() as session:
        session['usertype'] = usertype
    response = client.get(url)
    if(isinstance(status, int)):
        assert status == response.status_code
    else:
        assert bytes(status, 'utf-8') in response.data

def check_usertype_outliers(client, url:str='/') -> None:
    # case 1: usertype is random string
    trial = 50  # test 50 random strings as default
    for i in range(trial):
        check_usertype(client, url, random_string(), 'unauthorized for this url')
        
    # case 2: usertype is integer
    check_usertype(client, url, 4523, 'unauthorized for this url')
    check_usertype(client, url, -4523, 'unauthorized for this url')
    import sys
    check_usertype(client, url, sys.maxsize, 'unauthorized for this url')
    check_usertype(client, url, -sys.maxsize, 'unauthorized for this url')
    
    # case 3: usertype is boolean
    check_usertype(client, url, True, 'unauthorized for this url')
    check_usertype(client, url, False, 'unauthorized for this url')
    
    # case 4: usertype is None
    check_usertype(client, url, None, 'unauthorized for this url')

def logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'login.html' in response.data

############################## test functions ##############################
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    
def test_patient(client):
    # case 1: try access as Patient
    check_usertype(client, '/patient', 'patient')
    
    # case 2: try access as Physician
    check_usertype(client, '/patient', 'physician', 'unauthorized for this url')
    
    # case 3: try access as Pharmacy
    check_usertype(client, '/patient', 'pharmacy', 'unauthorized for this url')
    
    check_usertype_outliers(client, '/patient')

def test_physician(client):
    # case 1: try access as Patient
    check_usertype(client, '/patient', 'patient', 'unauthorized for this url')
    
    # case 2: try access as Physician
    check_usertype(client, '/patient', 'physician')
    
    # case 3: try access as Pharmacy
    check_usertype(client, '/patient', 'pharmacy', 'unauthorized for this url')
    
    check_usertype_outliers(client, '/physician')

def test_pharmacy(client):
    # case 1: try access as Patient
    check_usertype(client, '/patient', 'patient', 'unauthorized for this url')
    
    # case 2: try access as Physician
    check_usertype(client, '/patient', 'physician', 'unauthorized for this url')
    
    # case 3: try access as Pharmacy
    check_usertype(client, '/patient', 'pharmacy')
    
    check_usertype_outliers(client, '/pharmacy')

def test_login(app, client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'login.html' in response.data
    
    # case 1: log in as Patient
    with app.app_context():
        from ..db_classes import Patient
        patients = Patient.query.all()
        for patient in patients:
            user_info = { 'user':'patient', 'username':patient.username, 'password':patient.password }
            response = client.post('/login', data=user_info, follow_redirects=True)
            assert response.status_code == 200
            assert b'patient.html' in response.data
            logout(client)
    
    # case 2: log in as Physician
    with app.app_context():
        from ..db_classes import Physician
        physicians = Physician.query.all()
        for physician in physicians:
            user_info = { 'user':'physician', 'username':physician.username, 'password':physician.password }
            response = client.post('/login', data=user_info, follow_redirects=True)
            assert response.status_code == 200
            assert b'physician.html' in response.data
            logout(client)
    
    # case 3: log in as Pharmacy
    with app.app_context():
        from ..db_classes import Pharmacy
        pharmacies = Pharmacy.query.all()
        for pharmacy in pharmacies:
            user_info = { 'user':'pharmacy', 'username':pharmacy.username, 'password':pharmacy.password }
            response = client.post('/login', data=user_info, follow_redirects=True)
            assert response.status_code == 200
            assert b'pharmacist.html' in response.data
            logout(client)
    
    # case 4: try logging in with wrong info
    user_info = { 'user':'patient', 'username':'ABC', 'password':'1234' }
    response = client.post('/login', data=user_info, follow_redirects=True)
    assert response.status_code == 200
    assert b'login.html' in response.data
    
def test_get_patient_medications(app, client):
    with app.app_context():
        from flask import jsonify
        from ..db_classes import Patient
        from ..db_classes import Patient_medications
        
        # case 1: get patient medications of all patients in db
        patients = Patient.query.all()
        for patient in patients:
            response = client.get('/get_patient_medications/'+str(patient.id))
            assert response.status_code == 200
            if Patient_medications.query.filter_by(patient_id=patient.id).first():
                assert len(response.json[0]) > 0 or len(response.json[1]) > 0
            else:
                assert len(response.json[0]) == 0 and len(response.json[1]) == 0
            
        # case 2: wrong patient id
        import sys
        response = client.get('/get_patient_medications/'+str(sys.maxsize))
        assert response.status_code == 200
        # assert len(response.json[0]) == 0 and len(response.json[1]) == 0
        assert response.json == None

    # case 3: wrong routing usage
    response = client.get('/get_patient_medications/'+str(random_string()))
    assert response.status_code == 404
    
def test_get_patient_info(app, client):
    with app.app_context():
        from ..db_classes import Patient
        
        # case 1: get patient info of all patients in db
        patients = Patient.query.all()
        for patient in patients:
            response = client.get('/get_patient_info/'+str(patient.id))
            assert response.status_code == 200
            assert 'patient_info' in response.json
        
        # case 2: wrog patient id
        import sys
        response = client.get('/get_patient_info/'+str(sys.maxsize))
        assert response.status_code == 200
        assert response.json == None
    
    # case 3: wrong routing usage
    response = client.get('/get_patient_info/'+str(random_string()))
    assert response.status_code == 404
    
# test_indexing below is commented out as the way index is routed was changed since around April 30
# further development required if the project continues to scale up
# def test_indexing(app, client):
#     client.post('/login', data={ 'user':'physician', 'username':'AG','password':'1234' }, follow_redirects=True)
#     response = client.get('/', follow_redirects=True)
#     assert b'physician.html' in response.data