import requests,json

# dictionary containing device connection info
router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}

# dictionary containing RESTCONF headers
headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json"
}

# URL targetting capabilies data
base_url = f"https://{router['host']}:{router['port']}/restconf/data/netconf-state/capabilities"

# send request for capabilities data
response = requests.get(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False)

# if request status code is successful print list of capabilities
if response.status_code == 200:
    resp_dict = response.json()
    for capability in resp_dict['ietf-netconf-monitoring:capabilities']['capability']:
        print("*" * 25)
        print(capability)
