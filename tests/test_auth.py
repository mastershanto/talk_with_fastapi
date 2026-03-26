import os
import sys

TEST_DB_FILE = 'test_test.db'
os.environ['SQLALCHEMY_DATABASE_URL'] = f'sqlite:///{TEST_DB_FILE}'
if 'app.main' not in sys.modules and os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_login_todo():
    res = client.post('/auth/register', json={'username': 'u1', 'password': 'pass', 'email': 'a@b.com'})
    assert res.status_code == 201
    assert res.json()['username'] == 'u1'

    res = client.post('/auth/token', data={'username': 'u1', 'password': 'pass'})
    assert res.status_code == 200
    token = res.json()['access_token']
    assert token

    res = client.get('/todos')
    assert res.status_code == 401

    headers = {'Authorization': f'Bearer {token}'}
    res = client.get('/todos', headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
