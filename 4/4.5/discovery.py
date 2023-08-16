import json,requests,time

# REST API headers
headers = {
    "content-type": "application/json",
    "accept": "application/json"
}

# base URL for DNAC sandbox
baseURL = "https://sandboxdnac.cisco.com"

# Create a session object
dnac = requests.session()

cred_list= []
# list of credential types needed for device discovery
cred_types = ["CLI","SNMPV2_READ_COMMUNITY","SNMPV2_WRITE_COMMUNITY"]

# request auth token and store in headers
headers["X-Auth-Token"]=dnac.post(
    f"{baseURL}/dna/system/api/v1/auth/token",
    auth=("devnetuser","Cisco123!"),
    headers=headers,
    verify=False).json()["Token"]

# iterate over credential types and send a get request for each type
for cred in cred_types:
    cred_resp= dnac.get(
        f"{baseURL}/dna/intent/api/v1/global-credential",
        headers=headers,
        params={"credentialSubType": cred},
        verify=False)
    
    # print the output in human friendly format
    print(json.dumps(cred_resp.json(),indent=2))

    # get cred ID from response
    cred_id = cred_resp.json()["response"][0]["id"]

    # store credential ID in cred_list
    cred_list.append(cred_id)
    print(f"collected {cred} credential with ID {cred_id}")

# dictionary containing discovery data payload containing credential list
discovery={
                "name": "globo_ip",
                "discoveryType": "Range",
                "ipAddressList": "10.10.20.100-10.10.20.179",
                "timeOut": 1,
                "protocolOrder": "ssh,telnet",
                "preferredMgmtIPMethod": "None",
                "globalCredentialIdList": cred_list
        }

# send post request with discovery payload
disc_response = dnac.post(
    f"{baseURL}/dna/intent/api/v1/discovery",
    headers=headers,
    jsonbody=discovery,
    verify=False
    )     

# get the tast ID from the response
task= json.dumps(disc_response.json())["response"]["taskId"]                 

# get task progress
disc_id = json.dumps(dnac.get(f"{baseURL}/dna/intent/api/v1/task/{task}").json())["response"]["progress"]

# wait 15 seconds
time.sleep(15)

# get discovery data and print in human friendly format
get_disc = dnac.get(f"{baseURL}/dna/intent/api/v1/discovery/{disc_id}").json()

print(json.dumps(get_disc,indent=2))

