import requests
from requests.exceptions import HTTPError
import json

# base URL reaching out to sandbox DNAC controller
base_url = "https://sandboxdnac.cisco.com/dna"

# function for requesting authentication token from DNAC controller
def get_token():
    auth_url = f"{base_url}/system/api/v1/auth/token"
    user = "devnetuser"
    password = "Cisco123!"

    auth_header = {
        'content-type': "application/json"
    }

    try:
        auth_att = requests.post(url=f"{auth_url}", auth=(user, password), headers=auth_header, verify=False).json()['Token']
    except HTTPError as err_http:
        print(f"HTTP error occurred: \n ---> {err_http}")
    else:
        return auth_att

token = get_token()
# print(token)

# REST headers for DNAC controller containing authentication token
headers = {
    'x-auth-token': token,
    'accept': "application/json",
    'content-type': "application/json"
}

# URL targeting event resource
event_url = f"{base_url}/intent/api/v1/events?tags=ASSURANCE"

# send request to specified resource
event_resp = requests.get(url=f"{event_url}", headers=headers, verify=False).json()

# print json response in human friendly format
print(json.dumps(event_resp, indent=2))

event_list = ["NETWORK-DEVICES-3-252", "NETWORK-DEVICES-3-105"]

# JSON payload containing subscription data
payload = [
    {
        'name': "Test Sub",
        'subscriptionEndpoints':[
            {
                'subscriptionDetails': {
                    'connectorType': "REST",
                    'name': "Test Azure Python Function App",
                    'description': "Ingest payload into DB",
                    'method': "POST",
                    'url': "https://sometest.azurewebsites.net/DNA"
                }
            }
        ],
        'filter': {
            'eventIds': event_list
        }
    }
]

# URL targeting webhook event subscription resource
ev_sub_url = f"{base_url}/intent/api/v1/event/subscription"

# send post request with payload
event_sub_resp = requests.post(url=f"{ev_sub_url}", headers=headers, data=json.dumps(payload), verify=False)

# print response status code and text
print(event_sub_resp.status_code)
print(event_sub_resp.text)

