"""
Authentication System Documentation

Overview
--------
This application now includes a complete authentication system with JWT tokens,
password hashing, and user profile endpoints.

Files Added/Modified
--------------------

1. app/auth_utils.py (NEW)
   - Password hashing and verification using bcrypt
   - JWT token generation and decoding
   - Uses settings from app/config.py

2. app/repositories/auth.py (NEW)
   - AuthRepository class with methods:
     * get_user_by_email() - fetch user by email
     * verify_user_credentials() - validate email/password
     * create_user() - create new user with hashed password
     * generate_login_token() - generate JWT token

3. app/routers/auth.py (NEW)
   - POST /api/v1/auth/login - login with email and password
   - GET /api/v1/auth/profile - get current user profile

4. app/schemas/auth.py (NEW)
   - LoginRequest - request schema for login
   - UserResponse - user response schema
   - LoginResponse - login response with token
   - ProfileResponse - profile response schema

5. app/models/user.py (MODIFIED)
   - Added authentication fields:
     * email (unique, indexed)
     * password_hash
     * email_verified_at
     * role
     * Various profile fields (avatar, gender, age, weight, height, goal, etc.)

6. app/config.py (MODIFIED)
   - Added SECRET_KEY
   - Added ALGORITHM
   - Added ACCESS_TOKEN_EXPIRE_MINUTES

7. .env (MODIFIED)
   - Added SECRET_KEY
   - Added ALGORITHM
   - Added ACCESS_TOKEN_EXPIRE_MINUTES

8. requirements.txt (MODIFIED)
   - Added python-jose[cryptography]
   - Added passlib[bcrypt]
   - Added bcrypt
   - Added python-multipart

9. app/main.py (MODIFIED)
   - Imported auth router
   - Added auth router to application

Quick Start
-----------

1. Install dependencies:
   pip install -r requirements.txt

2. Run migrations (recreate tables with new schema):
   python scripts/migrate_db.py

3. Seed admin user:
   python scripts/seed_admin.py

4. Start the server:
   bash scripts/run.sh

API Endpoints
-------------

1. Login (POST /api/v1/auth/login)
   Request:
   {
       "email": "admin@gmail.com",
       "password": "password123"
   }
   
   Response (200):
   {
       "success": true,
       "message": "Login successful",
       "data": {
           "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
           "token_type": "bearer",
           "user": {
               "id": 1,
               "name": "Admin User",
               "email": "admin@gmail.com",
               "email_verified_at": "2026-03-12T09:49:21.000000Z",
               "role": "admin",
               "avatar": null,
               "agree_to_terms": true,
               "is_premium": false,
               "age": 23.0,
               "gender": "male",
               "height": 181.0,
               "weight": 62.0,
               "goal": "Gain muscle mass",
               ...
               "created_at": "2026-03-12T09:49:21.000000Z",
               "updated_at": "2026-03-12T09:49:21.000000Z"
           }
       },
       "code": 200
   }

2. Get Profile (GET /api/v1/auth/profile)
   (Note: In production, extract user_id from JWT token)
   
   Response (200):
   {
       "success": true,
       "message": "User data retrieved successfully",
       "data": {
           "id": 1,
           "name": "Admin User",
           "email": "admin@gmail.com",
           "avatar": null,
           "role": "admin",
           "agree_to_terms": true,
           "is_premium": false,
           "age": 23.0,
           "height": 181.0,
           "weight": 62.0,
           "gender": "male",
           "goal": "Gain muscle mass",
           ...
           "created_at": "2026-03-12T09:49:21.000000Z"
       },
       "code": 200
   }

Testing in Swagger UI
---------------------
1. Go to http://localhost:8000/docs
2. Find "Auth" section
3. Click "Try it out" on the login endpoint
4. Enter credentials:
   - Email: admin@gmail.com
   - Password: password123
5. Execute and view the response

Next Steps (Production Ready)
-----------------------------
1. Add Bearer token extraction from Authorization header
2. Create a dependency to validate and decode JWT tokens
3. Add current_user dependency to protected endpoints
4. Add token refresh endpoint
5. Add logout/token blacklist mechanism
6. Add email verification workflow
7. Add password reset functionality
8. Add role-based access control (RBAC)
9. Add rate limiting on login endpoint
10. Add user registration endpoint

Database Schema
---------------
New users table includes:
- Core fields: id, name, email, password_hash, role
- Authentication: email_verified_at
- Profile fields: avatar, age, gender, height, weight
- Fitness goals: goal, days_in_week, time_in_day, workout_duration
- Target metrics: target_bmi, target_body_fat, target_weight
- Preferences: agree_to_terms, is_premium
- Timestamps: created_at, updated_at (from TimestampMixin)

Security Notes
--------------
1. Passwords are hashed using bcrypt (never stored in plaintext)
2. JWT tokens are signed with SECRET_KEY from environment
3. Change SECRET_KEY in production! (Use `openssl rand -hex 32`)
4. Store SECRET_KEY securely (environment variable)
5. Always use HTTPS in production
6. Implement token expiration and refresh
7. Add rate limiting to login endpoint
"""
