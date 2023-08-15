import requests,json


# dictionary containing device connection info
router = {
    'host': "https://sandbox-iosxe-latest-1.cisco.com",
    'port': "443",
    'username': "admin",
    'password': "C1sco12345"
}

# dictionary containing RESTCONF headers
headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json"
}

# URL targetting all interfaces
base_url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces"

# send request for interface data
response = requests.get(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False).json()

# print response
print(json.dumps(response, indent=4))
