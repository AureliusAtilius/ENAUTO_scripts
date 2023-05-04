import requests,json


headers = {
    "content-type": "application/json",
    "accept": "application/json"
}

baseURL = "https://sandboxdnac.cisco.com"

dnac = requests.session()

headers["X-Auth-Token"]= dnac.post(f"{baseURL}/dna/system/api/v1/auth/token",headers=headers,auth=("devnetuser","Cisco123!"), verify = False).json()["Token"]


print(json.dumps(dnac.get(f"{baseURL}/dna/intent/api/v1/task/2861dc4d-65af-4ae8-a030-d0be5a7fb778",headers=headers,verify=False).json(),indent=2))