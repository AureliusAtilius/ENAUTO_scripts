import requests
import json

router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}

headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json"
}

base_url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces/"

response = requests.get(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False).json()

payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback55",
        "description": "Test Added Loopback",
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

response = requests.post(url=base_url, headers=headers, auth=(router['username'], router['password']), data=json.dumps(payload), verify=False)

if response.status_code == 201:
    print(response.text)
