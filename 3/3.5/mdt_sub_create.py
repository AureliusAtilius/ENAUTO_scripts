import json,requests


r = {
    'host': "10.10.20.48",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}
auth = (r["username"],r["password"])
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

xe = requests.session()

resp = xe.get(f"https://{r['host']}:443/restconf/data/Cisco-IOS-XE-config-data:mdt-config-data/",headers=headers,auth=auth,verify=False)

print(json.dumps(resp.json(),indent=2))

payload = {
    "mdt-subscription": [ 
        {
        
        "subscription-id": 100,
        "base": {
            "stream": "yang-push",
            "encoding": "encode-kvgpb",
            "period": 1000,
            "x-path": "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds"
            },
        "mdt-receivers": {
            "address": "10.10.20.50",
            "port": 5233,
            "protocol": "grpc-tcp"
        }
        
    }
    ]
}

print("Submitting mdt subscription")
resp = xe.post(f"https://{r['host']}:443/restconf/data/Cisco-IOS-XE-config-data:mdt-config-data/",data=json.dumps(payload),headers=headers,auth=auth,verify=False)

print(resp.status_code)

resp = xe.get(f"https://{r['host']}:443/restconf/data/Cisco-IOS-XE-config-data:mdt-config-data/",headers=headers,auth=auth,verify=False)

print(json.dumps(resp.json(),indent=2))