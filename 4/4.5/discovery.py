import json,requests,time


headers = {
    "content-type": "application/json",
    "accept": "application/json"
}

baseURL = "https://sandboxdnac.cisco.com"

dnac = requests.session()

cred_list= []
cred_types = ["CLI","SNMPV2_READ_COMMUNITY","SNMPV2_WRITE_COMMUNITY"]
headers["X-Auth-Token"]=dnac.post(
    f"{baseURL}/dna/system/api/v1/auth/token",
    auth=("devnetuser","Cisco123!"),
    headers=headers,
    verify=False).json()["Token"]
for cred in cred_types:
    cred_resp= dnac.get(
        f"{baseURL}/dna/intent/api/v1/global-credential",
        headers=headers,
        params={"credentialSubType": cred},
        verify=False)
    print(json.dumps(cred_resp.json(),indent=2))
    cred_id = cred_resp.json()["response"][0]["id"]
    cred_list.append(cred_id)
    print(f"collected {cred} credential with ID {cred_id}")

discovery={
                "name": "globo_ip",
                "discoveryType": "Range",
                "ipAddressList": "10.10.20.100-10.10.20.179",
                "timeOut": 1,
                "protocolOrder": "ssh,telnet",
                "preferredMgmtIPMethod": "None",
                "globalCredentialIdList": cred_list
        }

disc_response = dnac.post(
    f"{baseURL}/dna/intent/api/v1/discovery",
    headers=headers,
    jsonbody=discovery,
    verify=False
    )     

task= json.dumps(disc_response.json())["response"]["taskId"]                 

print(task)
disc_id = json.dumps(dnac.get(f"{baseURL}/dna/intent/api/v1/task/{task}").json())["response"]["progress"]
time.sleep(15)

get_disc = dnac.get(f"{baseURL}/dna/intent/api/v1/discovery/{disc_id}").json()

print(json.dumps(get_disc,indent=2))

