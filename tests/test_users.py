import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth('admin', 'admin')
USER1 = 'mike'
USER2 = 'admin'

def test_follows():
    r = requests.put(f'http://127.0.0.1:8000/v1/follow/{USER1}/', auth=AUTH)
    assert r.status_code == 201
    r = requests.put(f'http://127.0.0.1:8000/v1/follow/{USER1}/', auth=AUTH)
    assert r.status_code == 201

    r = requests.get(f'http://127.0.0.1:8000/v1/users/{USER2}/follows')
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = requests.get(f'http://127.0.0.1:8000/v1/users/{USER1}/followed')
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = requests.delete(f'http://127.0.0.1:8000/v1/follow/{USER1}/', auth=AUTH)
    assert r.status_code == 204
    r = requests.delete(f'http://127.0.0.1:8000/v1/follow/{USER1}/', auth=AUTH)
    assert r.status_code == 404
