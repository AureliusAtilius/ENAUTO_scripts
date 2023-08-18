import requests,json

# REST API headers
headers = {
    "content-type": "application/json",
    "accept": "application/json"
}

# URL for DNAC sandbox
baseURL = "https://sandboxdnac.cisco.com"

# create DNAC session
dnac = requests.session()

# get auth token and add to headers
headers["X-Auth-Token"]= dnac.post(f"{baseURL}/dna/system/api/v1/auth/token",headers=headers,auth=("devnetuser","Cisco123!"), verify = False).json()["Token"]

# request results of pathtrace using trace id and print response in human friendly format
print(json.dumps(dnac.get(f"{baseURL}/dna/intent/api/v1/flow-analysis/48e9f722-a56c-450c-a527-946e9c306a2f",headers=headers,verify=False).json(),indent=2))