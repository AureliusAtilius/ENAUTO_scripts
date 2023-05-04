import requests,json


headers = {
    "content-type": "application/json",
    "accept": "application/json"
}

baseURL = "https://sandboxdnac.cisco.com"

dnac = requests.session()

headers["X-Auth-Token"]= dnac.post(f"{baseURL}/dna/system/api/v1/auth/token",headers=headers,auth=("devnetuser","Cisco123!"), verify = False).json()["Token"]

print(json.dumps(dnac.get(f"{baseURL}/dna/intent/api/v1/flow-analysis/48e9f722-a56c-450c-a527-946e9c306a2f",headers=headers,verify=False).json(),indent=2))