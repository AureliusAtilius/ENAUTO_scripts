#!/usr/bin/env python

import json, time
from pathlib import Path
from dnac_requester import DNACRequester


def main():
    
    # create instance of DNACRequester using Cisco sandbox host
    dnac= DNACRequester(
        host="sandboxdnac.cisco.com", username="devnetuser", password="Cisco123!", verify=False, old_style=True
    )
    # get current working directory path
    cwp= Path.cwd()
    

    for body_type in ["area", "building", "floor"]:
        
        # open and load data from JSON files
        with open(f"{cwp}/4.4/site_data/{body_type}.json","r") as handle:
            data = json.load(handle)

        site = data["site"][body_type]
        name = f"{site['parentName']}/{site['name']}"

        print(f"Adding {body_type} object {name}")

        # post site data to DNAC controller
        add_resp = dnac.req(
            "dna/intent/api/v1/site", method="post", jsonbody=data
        )

        # get status URL and wait until site creation completes
        status_url= add_resp.json()["executionStatusUrl"]
        status_resp= wait_for_site_creation(dnac, status_url[1:])

        # site creation error handling
        if status_resp.json()["status"].lower() != "success":
            raise ValueError("Site object addition failed")
        
        # request site data of created site
        get_resp = dnac.req("dna/intent/api/v1/site", params={"name": name})
        obj_data = get_resp.json()["response"][0]


        if body_type == "floor": 
            floor_id = obj_data["id"]

        print(f"Object created with id {obj_data['id']}")

    # open and read device JSON file and load
    with open(f"site_data/device.json", "r") as handle:
        data = json.load(handle)

    # post device payload to add device
    add_dev_resp = dnac.req(
         "dna/intent/api/v1/network-device", method="post", jsonbody=data
    )

    # wait for device to be added
    dnac.wait_for_task(add_dev_resp.json()["repsonse"]["taskId"])

    # post IP address for created device
    new_ip = data["ipAddress"][0]
    assign_dev_resp = dnac.req(
         f"dna/system/api/v1/site/{floor_id}/device",
         method="post",
         jsonbody={"device": [{"ip": new_ip}]},
    )

    
    # get status URL and wait for site creation
    status_url = assign_dev_resp.json()["executionStatusUrl"]
    status_resp = wait_for_site_creation(dnac,status_url[1:])

    # get membership of floor
    mem_resp = dnac.req(f"dna/intent/api/v1/membership/{floor_id}")

    # check to see if the device IP was changed successfully
    added_ip = mem_resp.json()["device"][0]["response"][0]["managementIpAddress"]
    if new_ip != added_ip:
         raise ValueError("IP addresses don't match: {new_ip} != {added_ip}")
    
    print(f"Assigned device to floor {floor_id} with IP address {new_ip}")


# function for waiting for site creation to complete
def wait_for_site_creation(dnac, status_url, wait_time=5):
        done = False

        while not done:
            time.sleep(wait_time)

            status_resp = dnac.req(status_url)
            done = status_resp.json()["status"].lower() != "in_progress"
        return status_resp


if __name__=="__main__":
     main()