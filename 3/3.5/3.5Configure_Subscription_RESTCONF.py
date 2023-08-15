import requests
import json

# dictionary containing device connection info
router = {
    'host': "10.10.20.48",
    'port': "443",
    'username': "developer",
    'password': "C1sco12345"
}

# dictionary containing RESTCONF headers
headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json"
   }

# targeted module
module = "Cisco-IOS-XE-mdt-cfg:mdt-config-data/"

# URL targeting specified module
url = f"https://{router['host']}:{router['port']}/restconf/data/{module}"
print(url)
  
# RESTCONF payload in JSON format containing mdt subscription data  
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
        "protocol": "grpc-tcp",
        "address": "10.10.20.50",
        "port": 42518
      },
    }
  ]
}

# post payload to targeted resource
response = requests.post(url, headers=headers, data=json.dumps(payload), auth=(router['username'], router['password']), verify=False)

# print response
print(response)