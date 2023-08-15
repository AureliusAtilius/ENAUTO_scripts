import json,requests

# dictionary containing device connection info
r = {
    'host': "10.10.20.48",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}

# create tuple containing login credentials
auth = (r["username"],r["password"])

# dictionary containing RESTCONF headers
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}


# RESTCONF payload in JSON format containing mdt suscription data
payload = {
    "mdt-subscription": [ 
        {
        "subscription-id": 100,
        "base": {
            "stream": "yang-push",
            "encoding": "encode-kvgpb",
            "period": "1000",
            "xpath": "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds"
            },
        "mdt-receivers": {
            "address": "10.10.20.50",
            "port": 42518,
            "protocol": "grpc-tcp"
        }
        
    }
    ]
}

print("Submitting mdt subscription")
# send post with payload to create subscription
resp = requests.post(f"https://{r['host']}:443/restconf/data/Cisco-IOS-XE-mdt-cfg:mdt-config-data/",data=json.dumps(payload),headers=headers,auth=(r["username"],r["password"]),verify=False)

# print response status code and reason phase
print(resp.status_code)
print(resp.reason)

# send get request of mdt subscription data
resp = requests.get(f"https://{r['host']}:443/restconf/data/Cisco-IOS-XE-mdt-cfg:mdt-config-data/mdt-subscription",headers=headers,auth=(r["username"],r["password"]),verify=False)

# if there is anything returned by response, print response in human friendly format
if resp:
    print(json.dumps(resp.json(),indent=2))