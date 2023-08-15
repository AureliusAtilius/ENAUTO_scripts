import requests
import json


# dictionary containing device connection info
router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "443",
    'username': "admin",
    'password': "C1sco12345"
}

# RESTCONF headers
headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json"
}

# URL for reaching the device interfaces
base_url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces/"

# request the device info specified in the URL 
response = requests.get(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False).json()

# print json response in human readable format
print(json.dumps(response,indent=2))

# json payload for adding Looback100 interface
payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback100",
        "description": "I don't know if I'm going to pass ENAUTO",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.16.0.2",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
}

# send payload 
response = requests.post(url=base_url, headers=headers, auth=(router['username'], router['password']), data=json.dumps(payload), verify=False)

# print output if interface is created
if response.status_code == 201:
    print(response.text)
