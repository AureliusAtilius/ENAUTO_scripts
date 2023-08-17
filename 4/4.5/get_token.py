import requests
from requests.exceptions import HTTPError

# function for request auth token from DNAC controller
def get_token():
    base_url = "https://sandboxdnac.cisco.com/dna"
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

