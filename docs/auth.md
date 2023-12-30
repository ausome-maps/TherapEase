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
   curl -X GET -H "Content-type: application/json" -H "Authorization: Bearer {Bearer-Access-Token}" http://localhost:9001/auth/users/me
   ```

4. Logout

   ```bash
   curl -X POST -H "Authorization: Bearer {Bearer-Access-Token}" http://localhost:9001/auth/jwt/logout
   ```

## Other Functions

1. User Registration
   ```bash
   curl -X POST -H "Content-type: application/json" http://localhost:9001/auth/users/ -d '{"username":"sample@sample.com", "email": "sample@sample.com", "password": "mypassword1234", "first_name": "my-first-name", "last_name": "my-last-name"}'
   ```

2. User Activation
   ```bash
   curl -X POST http://localhost:9001/auth/users/activation/ -d '{"uid": "<uid>", "token":"<token>"}'
   ```
   NOTE: There must be a page in the frontend with the same values with the `DJOSER - ACTIVATION_URL` since this parameter will be sent to the user via email to activate their account.

3. Trigger the Password Reset Process
   ```bash
   curl -H "Content-type: application/json" -X POST http://localhost:9001/auth/users/reset_password/ -d '{"email": "sample@sample.com"}'
   ```
   NOTE: There must be a page in the frontend with the same values with the `DJOSER - PASSWORD_RESET_CONFIRM_URL` since this parameter will be sent to the user via email to reset their password. _If the user is not yet activated they will not receive an email._

4. Finish the Password Reset Process
   ```bash
   curl -X POST http://localhost:9001/auth/users/reset_password_confirm/ -d '{"uid": "<uid>", "token":"<token>", "new_password": "user-new-password", "re_new_password": "user-new-password"}'
   ```
   NOTE: This is triggered in the frontend when the user submits their new password.