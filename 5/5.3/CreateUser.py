from urllib import response
import requests


# function for requesting authentication token from SDWAN controller
def get_login(username, password):
    auth_url = f"{base_url}/j_security_check"

    login_body = {
        'j_username': username,
        'j_password': password
    }

    login_resp = sess.post(url=auth_url, data=login_body, verify=False)

    if login_resp.text:
        print("***** LOGIN FAILED *****")
        import sys
        sys.exit(1)
    else:
        print("***** LOGIN SUCCESS *****")
        return login_resp


# function for posting new user account to controller
def create_user(acct_username, acct_password):
        # URL targeting user administration on controller
        acct_url=f"{base_url}/dataservice/admin/user"

        # payload containing user account info
        payload={
                'group':["netadmin"],
                'description':'Test User200',
                'userName':acct_username,
                'password':acct_password
        }

        # REST headers
        headers={
                'Accept':'application/json',
                'Content-Type':'application/json'
        }

        # post payload request and print response
        response=sess.post(url=acct_url,headers=headers,data=payload,verify=False)
        print(response)



# function for updating user account info 
def update_user_pw(acct_username, acct_password):
        # URL targetting user password
        acct_url=f"{base_url}/dataservice/admin/user/password/test"

        # payload with username and new password
        payload={
                'userName':acct_username,
                'password':acct_password
        }

        # REST headers
        headers={
                'Accept':'applictation/json',
                'Content-Type':'application/json'
        }

        # post payload request and print response
        response= sess.post(url=acct_url,headers=headers,data=payload,verify=False)
        print(response)


if __name__=="__main__":
        # base URL for SDWAN sandbox controller
        base_url = "https://sandbox-sdwan-2.cisco.com"
        # create session object
        sess = requests.session()
        # request authentication for session
        token = get_login('devnetuser', 'RG!_Yw919_83')
        # create user
        create_user("test","Pass123!")
        # change user password
        update_user_pw("test","!321ssap")