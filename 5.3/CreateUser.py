from urllib import response
import requests

#base_url = "https://sandbox-sdwan-2.cisco.com"
#sess = requests.session()

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

#token = get_login('devnetuser', 'RG!_Yw919_83')


def create_user(acct_username, acct_password):
        acct_url=f"{base_url}/dataservice/admin/user"

        payload={
                'group':["netadmin"],
                'description':'Test User200',
                'userName':acct_username,
                'password':acct_password
        }

        headers={
                'Accept':'application/json',
                'Content-Type':'application/json'
        }
        response=sess.post(url=acct_url,headers=headers,data=payload,verify=False)
        print(response)

#create_user("test","Pass123!")


def update_user_pw(acct_username, acct_password):
        acct_url=f"{base_url}/dataservice/admin/user/password/test"

        payload={
                'userName':acct_username,
                'password':acct_password
        }

        headers={
                'Accept':'applictation/json',
                'Content-Type':'application/json'
        }

        response= sess.post(url=acct_url,headers=headers,data=payload,verify=False)
        print(response)


if __name__=="__main__":
        base_url = "https://sandbox-sdwan-2.cisco.com"
        sess = requests.session()
        token = get_login('devnetuser', 'RG!_Yw919_83')
        create_user("test","Pass123!")
        update_user_pw("test","!321ssap")