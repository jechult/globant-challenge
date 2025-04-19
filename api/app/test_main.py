from fastapi.testclient import TestClient
from main import app
from oauth2 import create_access_token
from constants import API_USER, API_PASSWORD
import os

client = TestClient(app)

temp_token = create_access_token(
    data = {"user_id": API_USER}
)

def test_login_ok():
    response = client.post(
        "/login",
        data = {
            "username" : API_USER,
            "password" : API_PASSWORD
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

def test_login_failed():
    response = client.post(
        "/login",
        data = {
            "username" : "otheruser",
            "password" : "otherpass"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == 'Invalid credentials'

def test_upload_file_job():
    filename = "test_files/Jobs.csv"
    table_name = 'job'

    files = {'table_content': open(filename, 'rb')}

    response = client.post(
        '/loadfile',
        data = {
            'table_name': table_name
        },
        files = files,
        headers = {
            "Authorization": f"Bearer {temp_token}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json().keys()

def test_upload_file_department():
    filename = "test_files/departments.csv"
    table_name = 'department'

    files = {'table_content': open(filename, 'rb')}

    response = client.post(
        '/loadfile',
        data = {
            'table_name': table_name
        },
        files = files,
        headers = {
            "Authorization": f"Bearer {temp_token}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json().keys()

def test_upload_file_hired_employee():
    filename = "test_files/hired_employees.csv"
    table_name = 'hired_employee'

    files = {'table_content': open(filename, 'rb')}

    response = client.post(
        '/loadfile',
        data = {
            'table_name': table_name
        },
        files = files,
        headers = {
            "Authorization": f"Bearer {temp_token}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json().keys()

def test_reporting_1():

    response = client.get(
        '/reporting/hired_employee_per_quarter',
        params = {
            'reporting_year': 2021
        },
        headers = {
            "Authorization": f"Bearer {temp_token}"
        }
    )

    assert response.status_code == 200

def test_reporting_2():

    response = client.get(
        '/reporting/department_hired_employee_more_than_mean',
        params = {
            'reporting_year': 2021
        },
        headers = {
            "Authorization": f"Bearer {temp_token}"
        }
    )

    assert response.status_code == 200