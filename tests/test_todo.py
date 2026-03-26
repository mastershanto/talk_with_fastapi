import os
import sys

TEST_DB_FILE = 'test_test.db'
os.environ['SQLALCHEMY_DATABASE_URL'] = f'sqlite:///{TEST_DB_FILE}'
if 'app.main' not in sys.modules and os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_todo_crud():
    client.post('/auth/register', json={'username': 'tuser', 'password': 'pass', 'email': 't@t.com'})
    r = client.post('/auth/token', data={'username': 'tuser', 'password': 'pass'})
    assert r.status_code == 200
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    r = client.post('/todos', json={'title': 'T1', 'description': 'D1'}, headers=headers)
    assert r.status_code == 201
    tid = r.json()['id']

    r = client.get(f'/todos/{tid}', headers=headers)
    assert r.status_code == 200

    r = client.put(f'/todos/{tid}', json={'title': 'T2', 'description': 'D2', 'completed': True}, headers=headers)
    assert r.status_code == 200
    assert r.json()['title'] == 'T2'

    r = client.delete(f'/todos/{tid}', headers=headers)
    assert r.status_code == 204

    r = client.get(f'/todos/{tid}', headers=headers)
    assert r.status_code == 404
