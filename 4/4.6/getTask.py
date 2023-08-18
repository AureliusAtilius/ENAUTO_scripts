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

# request status of an asynchronous task using the task ID
print(json.dumps(dnac.get(f"{baseURL}/dna/intent/api/v1/task/2861dc4d-65af-4ae8-a030-d0be5a7fb778",headers=headers,verify=False).json(),indent=2))