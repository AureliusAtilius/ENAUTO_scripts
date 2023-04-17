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

module = "Cisco-IOS-XE-mdt-cfg:mdt-config-data/mdt-subscription=100/base"

url = f"https://{router['host']}:{router['port']}/restconf/data/{module}"
print(url)
  
payload = {
  "base": {
    "stream": "yang-push",
    "encoding": "encode-kvgpb",
    "period": "2000",
    "xpath": "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds"
  }
}
print(payload)

response = requests.put(url, headers=headers, data=json.dumps(payload), auth=(router['username'], router['password']), verify=False)

print(response)