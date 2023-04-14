import requests
import json

router = {
    'host': "10.10.20.48",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}

headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json"
   }

module = "Cisco-IOS-XE-mdt-cfg:mdt-config-data/mdt-subscription"

url = f"https://{router['host']}:{router['port']}/restconf/data/{module}"
print(url)
  
payload = {
      "subscription-id": 100,
      "base": {
        "stream": "yang-push",
        "encoding": "encode-kvgpb",
        "period": 1000,
        "xpath": "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds",
      },
      "mdt-receivers": {
        "protocol": "grpc-tcp",
        "address": "10.10.20.50",
        "port": 42518
      }
    }
  
print(payload)

response = requests.put(url, headers=headers, data=json.dumps(payload), auth=(router['username'], router['password']), verify=False)

print(json.dumps(response.json(),indent=2))