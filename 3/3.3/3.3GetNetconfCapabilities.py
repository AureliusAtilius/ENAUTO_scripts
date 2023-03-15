import requests,json

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

base_url = f"https://{router['host']}:{router['port']}/restconf/data/netconf-state/capabilities"

response = requests.get(url=base_url, headers=headers, auth=(router['username'], router['password']), verify=False)

if response.status_code == 200:
    resp_dict = response.json()
    for capability in resp_dict['ietf-netconf-monitoring:capabilities']['capability']:
        print("*" * 25)
        print(capability)
