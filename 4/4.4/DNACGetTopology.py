import requests
from requests.exceptions import HTTPError
import json


# base URL using DNAC sandbox
base_url = "https://sandboxdnac.cisco.com/dna"

# funtion for retrieving auth token
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

# get token for session
token = get_token()

# REST API headers containing auth token
headers = {
    'x-auth-token': token,
    'accept': "application/json",
    'content-type': "application/json"
}

# URL for requesting site topology 
get_topologyURL="https://sandboxdnac.cisco.com/dna/intent/api/v1/topology/site-topology"

# send get request
response=event_resp = requests.get(url=f"{get_topologyURL}", headers=headers, verify=False).json()

# print response in human friendly format
print(json.dumps(response, indent=2))