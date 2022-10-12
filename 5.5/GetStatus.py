import requests
import json

def get_login(username, password):
    auth_url = f"{base_url}/j_security_check"

    login_body = {
        'j_username': username,
        'j_password': password
    }

    login_resp = sess.post(url=auth_url, data=login_body, verify=False)

    if not login_resp.ok or login_resp.text:
        print("***** LOGIN FAILED *****")
        import sys
        sys.exit(1)
    else:
        print("***** LOGIN SUCCESS *****")
        return login_resp

def get_status(url):
        status_urls={
                'certs':f"{base_url}/dataservice/certificate/stats/summary",
                'alarms':f"{base_url}/dataservice/alarms/count",
                'vpn-tun':f"{base_url}/dataservice/device/tunnel/statistics?deviceId=<IP Address>"#Real-time
        }

        response=sess.get(url=status_urls[url],verify=False).json()
        print(json.dumps(response,indent=2))

if __name__=="__main__":
        base_url = "https://sandbox-sdwan-2.cisco.com"
        sess = requests.session()
        token = get_login("devnetuser", "RG!_Yw919_83")
        get_status('alarms')

