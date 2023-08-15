import requests

urls = "http://localhost:9001"
data = {"name": "hello", "email": "root12@admin.com", "password": "rootpassword1234"}
r = requests.post(urls + "/auth/register", json=data)
data = {"username": "root12@admin.com", "password": "rootpassword1234"}
r = requests.post(urls + "/auth/jwt/login", data=data)
access_token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}
r = requests.get(urls + "/users/me", headers=headers)
if r.status_code == 200:
    print(r.json())
