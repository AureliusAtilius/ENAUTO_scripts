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

# URL targetting interface Loopback55
base_url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces/interface=Loopback55"

# send delete request
response = requests.delete(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False).json()

# print response
print(response)
