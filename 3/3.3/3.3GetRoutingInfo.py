import requests,json

router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "443",
    'username': "admin",
    'password': "C1sco12345"
}

headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json"
}

base_url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-routing:routing"

response = requests.get(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False).json()
print(json.dumps(response, indent=4))
