import requests
import json

router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}

headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json"
   }

module = "Cisco-IOS-XE-mdt-cfg:mdt-config-data"

url = f"https://{router['host']}:{router['port']}/restconf/data/{module}"
print(url)

payload = {
    "mdt-config-data": {
        "mdt-subscription": {
                "subscription-id": 100,
                "base": {
                    "stream": "yang-push",
                    "encoding": "encode-kvgpb",
                    "xpath": "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds",
                    "period": 1000
                },
                "mdt-receivers": {
                    "address": "10.0.19.188",
                    "port": 42518,
                    "protocol": "grpc-tcp"
                }
            }
        }
}

print(payload)

response = requests.post(url, headers=headers, data=json.dumps(payload), auth=(router['username'], router['password']), verify=False)
