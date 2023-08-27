# Auth Docs

The following is how you can work with the auth service.

## Authentication Flow

The flow of authentication are the following

1. User Login

   ```bash
      curl -v \
      -H "Content-Type: multipart/form-data" \
      -X POST \
      -F "username=sample@sample.com" \
      -F "password=mypassword1234" \
      http://localhost:9001/auth/jwt/login
   ```

2. Refreshing an access token token

   ```bash
   curl -X POST -H "Authorization: Bearer {Bearer-Access-Token}" http://localhost:9001/auth/jwt/refresh
   ```

3. Retrieve User Profile

   ```bash
   curl -X GET -H "Content-type: application/json" -H "Authorization: Bearer {Bearer-Access-Token}" http://localhost:9001/users/me
   ```

4. Logout

   ```bash
   curl -X POST -H "Authorization: Bearer {Bearer-Access-Token}" http://localhost:9001/auth/jwt/logout
   ```

## Other Functions

1. Registering/Creating a user

   ```bash
   curl -X POST -H "Content-type: application/json" http://localhost:9001/auth/register -d '{"name":"sample name", "email": "sample@sample.com", "password": "mypassword1234", "passwordConfirm": "mypassword1234"}'
   ```
