import requests
import json

# dictionary containing device connection data
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

# targetted module
module = "Cisco-IOS-XE-mdt-cfg:mdt-config-data/mdt-subscription=100/base"

# URL targetting specified module
url = f"https://{router['host']}:{router['port']}/restconf/data/{module}"

# RESTCONF payload in JSON format containing changes to existing subscription 
payload = {
  "base": {
    "stream": "yang-push",
    "encoding": "encode-kvgpb",
    "period": "2000",
    "xpath": "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds"
  }
}

# send put request with payload
response = requests.put(url, headers=headers, data=json.dumps(payload), auth=(router['username'], router['password']), verify=False)

#print response
print(response)