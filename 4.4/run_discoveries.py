#!/usr/bin/env python

import json 
import time
import os
from dnac_requester import DNACRequester

def main():
    

    dnac = DNACRequester(
        host="sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False,
        old_style=True
    )

    cred_list=[]
    cred_types = ["CLI", "SNMPV2_READ_COMMUNITY", "SNMPV2_WRITE_COMMUNITY"]
    for cred in cred_types:
        cred_resp= dnac.req(
            "dna/intent/api/v1/global-credential",
            params={"credentialSubType": cred}
        )
        print(json.dumps(cred_resp.json(), indent=2))
        cred_id = cred_resp.json()["response"][0]["id"]
        cred_list.append(cred_id)
        print(f"Collected {cred} credential with ID {cred_id}")

    
    with open("discoveries.json", "r") as handle:
        discoveries=json.load(handle)

    for disc_body in discoveries:
        disc_body["globalCredentialIdList"] = cred_list
        run_discovery(dnac, disc_body)

def run_discovery(dnac, disc_body, timeout=600):

    disc_resp = dnac.req(
        "dna/intent/api/v1/discovery", method="post", jsonbody=disc_body
    )

    disc_task = dnac.wait_for_task(disc_resp.json()["response"]["taskId"])
    disc_id = disc_task.json()["response"]["progress"]

    success = False
    for i in range(timeout // 10):

        get_disc = dnac.req(f"dna/intent/api/v1/discovery/{disc_id}")
        data = get_disc.json()["response"]


        if data["discoveryCondition"].lower() != "complete":
            print(f"Discovery {disc_id} {data['discoveryCondition']} {i}") 
            time.sleep(10)

        else: 
            print(f"Discovery {disc_id} found {data['numDevices']} devices")
            success = True
            break


    if not success:
        raise TimeoutError("Discovery did not complete in time")
    
    file_dir = f"disc_output/{disc_id}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    dev_sum = dnac.req(f"dna/intent/api/v1/discovery/{disc_id}/network-device")

    for dev in dev_sum.json()["response"]:

        if dev["reachabilityStatus"].lower() == "success":
            print(f"{dev['hostname']} success")

            if dev ["inventoryReachabilityStatus"].lower() == "reachable":
                get_dev = dnac.req(
                    f"dna/intent/api/v1/network-device/{dev['id']}"
                )

                output = {"discovery": dev, "device": get_dev.json()["response"]}
                with open(f"{file_dir}/{dev['hostname']}.json","w") as handle:
                    json.dump(output,handle, indent=2)

        else:
            print(
                f"Device {dev['managementIpAddress']}"
                f"failed: {dev['reachabilityFailureReason']}"
            )

if __name__=="__main__":
    main()