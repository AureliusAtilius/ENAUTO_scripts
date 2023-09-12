import requests
import json

# function for retrieving authentication token
def get_login(username, password):
    auth_url = f"{base_url}/j_security_check"

    # payload containing login credentials
    login_body = {
        'j_username': username,
        'j_password': password
    }

    # post payload to authentication resource
    login_resp = sess.post(url=auth_url, data=login_body, verify=False)

    # check if login was successful, if so, return token
    if not login_resp.ok or login_resp.text:
        print("***** LOGIN FAILED *****")
        import sys
        sys.exit(1)
    else:
        print("***** LOGIN SUCCESS *****")
        return login_resp

# function for retrieving certificate stats, alarm count, and device tunnel statistics.
def get_status(url):
        # dictionary containing three different URLs for different checks
        status_urls={
                'certs':f"{base_url}/dataservice/certificate/stats/summary",
                'alarms':f"{base_url}/dataservice/alarms/count",
                'vpn-tun':f"{base_url}/dataservice/device/tunnel/statistics?deviceId=<IP Address>"#Real-time, add device IP before running
        }
        # send get request to specified resource
        response=sess.get(url=status_urls[url],verify=False).json()

        # print response in human friendly format
        print(json.dumps(response,indent=2))

if __name__=="__main__":
        base_url = "https://sandbox-sdwan-2.cisco.com"
        sess = requests.session()
        token = get_login("devnetuser", "RG!_Yw919_83")
        get_status('alarms')

