import requests
import json

# URL for Cisco SDWAN sandbox
base_url = "https://sandbox-sdwan-2.cisco.com"
sess = requests.session()

# function for authenticating to controller
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
        
# authenticate to controller
token = get_login('devnetuser', 'RG!_Yw919_83')

# function for returning output containing device inventory, or device health
def device_output(url):
        device_urls = {
        'dev_list': f"{base_url}/dataservice/device",
        'dev_list_verbose': f"{base_url}/dataservice/system/device/vedges",
        'dev_health': f"{base_url}/dataservice/monitor",
        }
        headers = {
        'content-type': "application/json"
        }
        response = sess.get(url=device_urls[url], headers=headers, verify=False)
        return(response)

# request device list and print output in human friendly format       
device_inv = device_output('dev_list').json()
print(json.dumps(device_inv, indent=2))