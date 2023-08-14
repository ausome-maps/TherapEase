# Auth Docs

The following is how you can work with the auth service.

1. Retrieving the access token

   ```bash
   curl -X POST -H http://localhost:9001/auth
   ```

2. Refreshing a token

   ```bash
   curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7ImVtYWlsIjoic2FtcGxlQHNhbXBsZS5jb20iLCJyb2xlIjoidXNlciJ9LCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NDU3MzU4MiwiaWF0IjoxNjkxODk1MTgyLCJqdGkiOiJlYmMyYzIwMy1lY2U5LTQ4YjktODJkYi1hMDRhNzY3NTIxNDEifQ.qxQMdwAAXLQDFxMOC_Tq_hRO9DjXVXuX3bbHPP_qmrU" http://localhost:9001/refresh
   ```

3. Registering/Creating a user

   ```bash
   curl -X POST -H "Content-type: application/json" http://localhost:9001/register -d '{"name":"sample name", "email": "sample3@sample.com", "password": "mypassword1234", "passwordConfirm": "mypassword1234"}'
   ```

4. User Login

   ```bash
   curl -X POST -H "Content-type: application/json" http://localhost:9001/login -d '{"email":"sample3@sample.com", "password": "mypassword1234"}'
   ```

5. Retrieve User Profile

   ```bash
   curl -X GET -H "Content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYW1wbGUzQHNhbXBsZS5jb20iLCJleHAiOjE2OTE5NzY0MzJ9.MOKotUTIWrpqSIAMwaDIvl6LJmsKFJckZ8pXIlnphO0" http://localhost:9001/users/protected
   ```
