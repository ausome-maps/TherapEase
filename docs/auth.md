# Auth Docs

The following is how you can work with the auth service.

1. Retrieving the access token

   ```bash
   curl -X POST -H http://localhost:9001/auth
   ```

2. Refreshing a token
   ```bash
   curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoidXNlcm5hbWUiLCJyb2xlIjoidXNlciJ9LCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NDUwMzMwOSwiaWF0IjoxNjkxODI0OTA5LCJqdGkiOiI5NzlmZGYzMS0zODU1LTRkYzctYjhiZi1hMjFmM2U2OTg5YTYifQ.9Qwg1iNx55kVZPbLsJ62Y-tIKWTHhfyrLIKPvm6COfw" http://localhost:9001/refresh
   ```
3. Registering/Creating a user
   ```bash
   curl -X POST -H "Content-type: application/json" http://localhost:9001/register -d '{"name":"sample name", "email": "sample@sample.com", "password": "mypassword1234", "passwordConfirm": "mypassword1234", "photo": "photo.jpg"}'
   ```

4. User Login
   ```bash
   curl -X POST -H "Content-type: application/json" http://localhost:9001/login -d '{"email":"sample@sample.com", "password": "mypassword1234"}'
   ```
