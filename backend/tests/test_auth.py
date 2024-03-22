import os
import requests
from dotenv import load_dotenv 
import pytest 

from .init_tests import BASE_URL

"""
    * Get Session ID [/]
    * Sign Up [/]
    * Log In (Wrong Email) [/]
    * Log In (Wrong Password) [/]
    * Log In (Correct Credentials) [/]
    * User (Logged In) [/]
    * Log Out 
    * Generate Verification Code [/] - handled by sign up 
    * Check Verification Code (Right) [/] - handled by sign up
    * Check Verification Code (Wrong) [/] 
    * Forgot Password (E-mail Does Not Exist) [/]
    * Forgot Password (E-mail Exists) [/]
"""

class Actions:
    session_list = []

    def sign_up(**kwargs):
        # Get SMS Code  
        sms_vc_response = \
            requests.get(
                f"{BASE_URL}/auth/generate-verif-code?" + 
                f"type=mobile&" +
                f"handle=09123456789"    
            ) 
        sms_vc_response_json = sms_vc_response.json() 
        sms_code = sms_vc_response_json["code"]["value"]

        # Get Email Code
        email_vc_response = \
            requests.get(
                f"{BASE_URL}/auth/generate-verif-code?" +
                f"type=mobile&" +
                f"handle=johndoe@example.com"    
            )
        email_vc_response_json = email_vc_response.json() 
        email_code = email_vc_response_json["code"]["value"] 

        # Check Verification Codes 
        assert len(email_code) == 6 
        assert len(sms_code) == 6 

        check_email_code = \
            requests.post(
                f"{BASE_URL}/auth/verify-code?" + 
                f"handle=johndoe@example.com&" +
                f"code={email_code}"
            )

        check_sms_code = \
            requests.post(
                f"{BASE_URL}/auth/verify-code?" + 
                f"handle=09123456789&" +
                f"code={sms_code}"
            )

        check_email_code_json = check_email_code.json() 
        check_sms_code_json = check_sms_code.json()

        assert check_email_code_json["status"] == "VALID_CODE" 
        assert check_sms_code_json["status"] == "VALID_CODE"

        # Sign Up 
        sign_up = \
            requests.post(
                f"{BASE_URL}/auth/sign-up", 
                json={
                    "username" : "johndoe", 
                    "email" : "johndoe@example.com", 
                    "password" : "@JohnDoe1234();", 
                    "birthdate" : "2000-01-01 00:00:00", 
                    "gender" : "M", 
                    "region" : "V", 
                    "province" : "CAS",
                    "email_code" : email_code, 
                    "mobile_no" : "09123456789",
                    "sms_code" : sms_code 
                }
            ) 

        sign_up_json = sign_up.json() 

        assert sign_up_json["status"] == "REGISTERED"

    def unregister(): 
        from modules.repositories.users import users
        users.coll.delete_one({ "auth.username" : "johndoe" })

    def get_session_id(): 
        response = requests.get(f"{BASE_URL}/auth/session-id")
        session_id = response.cookies.get("SESSION_ID")
        return session_id

    def login(func = None):
        session_id = Actions.get_session_id() 

        Actions.session_list.append(session_id)
        
        Actions.sign_up() 
        
        log_in = \
            requests.post(
                f"{BASE_URL}/auth/log-in",
                json = {
                    "email" : "johndoe@example.com",
                    "password" : "@JohnDoe1234();"
                },
                cookies = {
                    "SESSION_ID" : session_id
                }
            )

        log_in_json = log_in.json() 

        assert log_in_json["status"] == "LOGGED_IN"

        return session_id

    def clear_sessions():
        from modules.main.auth import auth 
        for session_id in Actions.session_list: 
            auth.clear_session_user(session_id)

    def post_test(): 
        Actions.unregister()
        Actions.clear_sessions() 

class TestAuth: 
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        yield
        Actions.post_test()

    def test_can_get_session_id(self): 
        response = requests.get(f"{BASE_URL}/auth/session-id")
        session_id = response.cookies.get("SESSION_ID")
        assert len(session_id) == 36
        assert type(session_id) == str

    def test_can_sign_up(self): 
        Actions.sign_up()

    def test_check_verification_code(self): 
        response = \
            requests.post(
                f"{BASE_URL}/auth/verify-code?" + 
                f"handle=johndoe@example.com&" + 
                f"code=000000"
            )
        response_json = response.json() 
        assert response_json["status"] == "INVALID_CODE"

    def test_login_wrong_email(self): 
        from modules.repositories.users import users 
        Actions.sign_up()
        log_in = \
            requests.post(
                f"{BASE_URL}/auth/log-in",
                json = {
                    "email" : "johndoe@unknown.com",
                    "password" : "123456"
                }
            )
        log_in_json = log_in.json() 
        assert log_in_json["status"] == "EMAIL_DOES_NOT_EXIST"

    
    def test_login_wrong_password(self): 
        from modules.repositories.users import users 
        Actions.sign_up()
        log_in = \
            requests.post(
                f"{BASE_URL}/auth/log-in",
                json = {
                    "email" : "johndoe@example.com",
                    "password" : "123456"
                }
            )
        log_in_json = log_in.json()
        assert log_in_json["status"] == "INVALID_PASSWORD"

    def test_login_correct_credentials(self):
        Actions.login()

    def test_forgot_password(self): 
        Actions.sign_up(unregister=True)
        forget_password = \
            requests.get(
                f"{BASE_URL}/auth/forgot-password?" + 
                f"email=johndoe@example.com"
            ) 
        forget_password_json = forget_password.json()
        assert forget_password_json["status"] == "TEMPORARY_PASSWORD_SENT"

    def test_forgot_password_email_not_exists(self): 
        Actions.sign_up(unregister=True)
        forget_password = \
            requests.get(
                f"{BASE_URL}/auth/forgot-password?" + 
                f"email=johndoe@unknown.com"
            ) 
        forget_password_json = forget_password.json()
        assert forget_password_json["status"] == "EMAIL_DOES_NOT_EXIST"

    def test_user_logged_in(self):
        session_id = Actions.login() 
        user = \
            requests.get(
                f"{BASE_URL}/auth/user",
                cookies = {
                    "SESSION_ID" : session_id
                }
            )
        user_json = user.json() 
        assert user_json["data"]["auth"]["username"] == "johndoe"

    def test_user_not_logged_in(self): 
        user = \
            requests.get(
                f"{BASE_URL}/auth/user"
            )
        user_json = user.json()
        assert user_json["status"] == "USER_NOT_LOGGED_IN"

    def test_logout(self): 
        session_id = Actions.login()

        # get user details
        user = \
            requests.get(
                f"{BASE_URL}/auth/user",
                cookies = {
                    "SESSION_ID" : session_id
                }
            )
        user_json = user.json()
        assert user_json["data"]["auth"]["username"] == "johndoe"

        # log out user 
        logout = \
            requests.get(
                f"{BASE_URL}/auth/log-out", 
                cookies = {
                    "SESSION_ID" : session_id 
                }
            )
        logout_json = logout.json()
        assert logout_json["status"] == "USER_LOGGED_OUT"

        # check if user is logged out 
        user = \
            requests.get(
                f"{BASE_URL}/auth/user",
                cookies = {
                    "SESSION_ID" : session_id
                }
            )
        user_json = user.json()
        assert user_json["status"] == "USER_NOT_LOGGED_IN"