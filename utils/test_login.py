import requests

urls = "http://localhost:9001"

data = {"username": "sample@sample.com", "password": "mypassword1234"}

r = requests.post(urls + "/auth/jwt/login", data=data)
access_token = r.json()["access_token"]
print(access_token)
headers = {"Authorization": f"Bearer {access_token}"}
r = requests.get(urls + "/users/me", headers=headers)
print(r.json())