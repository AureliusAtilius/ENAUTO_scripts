import requests
import json

base_url = "https://sandbox-sdwan-2.cisco.com"
sess = requests.session()

headers={
    "Content-Type": "application/json",
    "Accept": "application/json"
}
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

token = get_login('devnetuser', 'RG!_Yw919_83')

print(json.dumps(sess.get(f"{base_url}/dataservice/template/policy/vsmart",headers=headers,verify=False).json(),indent=2))