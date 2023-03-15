#!/usr/bin/env python

import json, time
from pathlib import Path
from dnac_requester import DNACRequester


def main():
    

    dnac= DNACRequester(
        host="sandboxdnac.cisco.com", username="devnetuser", password="Cisco123!", verify=False, old_style=True
    )
    cwp= Path.cwd()
    
    for body_type in ["area", "building", "floor"]:
        
        with open(f"{cwp}/4.4/site_data/{body_type}.json","r") as handle:
            data = json.load(handle)

        site = data["site"][body_type]
        name = f"{site['parentName']}/{site['name']}"

        print(f"Adding {body_type} object {name}")

        add_resp = dnac.req(
            "dna/intent/api/v1/site", method="post", jsonbody=data
        )


        status_url= add_resp.json()["executionStatusUrl"]
        status_resp= wait_for_site_creation(dnac, status_url[1:])

        if status_resp.json()["status"].lower() != "success":
            raise ValueError("Site object addition failed")
        
        get_resp = dnac.req("dna/intent/api/v1/site", params={"name": name})
        obj_data = get_resp.json()["response"][0]


        if body_type == "floor": 
            floor_id = obj_data["id"]

        print(f"Object created with id {obj_data['id']}")

    with open(f"site_data/device.json", "r") as handle:
        data = json.load(handle)

    add_dev_resp = dnac.req(
         "dna/intent/api/v1/network-device", method="post", jsonbody=data
    )

    dnac.wait_for_task(add_dev_resp.json()["repsonse"]["taskId"])

    new_ip = data["ipAddress"][0]
    assign_dev_resp = dnac.req(
         f"dna/system/api/v1/site/{floor_id}/device",
         method="post",
         jsonbody={"device": [{"ip": new_ip}]},
    )

    

    status_url = assign_dev_resp.json()["executionStatusUrl"]
    status_resp = wait_for_site_creation(dnac,status_url[1:])

    mem_resp = dnac.req(f"dna/intent/api/v1/membership/{floor_id}")

    added_ip = mem_resp.json()["device"][0]["response"][0]["managementIpAddress"]
    if new_ip != added_ip:
         raise ValueError("IP addresses don't match: {new_ip} != {added_ip}")
    
    print(f"Assigned device to floor {floor_id} with IP address {new_ip}")



def wait_for_site_creation(dnac, status_url, wait_time=5):
        done = False

        while not done:
            time.sleep(wait_time)

            status_resp = dnac.req(status_url)
            done = status_resp.json()["status"].lower() != "in_progress"
        return status_resp


if __name__=="__main__":
     main()