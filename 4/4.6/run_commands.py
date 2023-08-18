#!/usr/bin/env python

import json,os
from pathlib import Path
from dnac_requester import DNACRequester

def main():
    
    # invoke instance of DNACRequester using DNAC sandbox
    dnac = DNACRequester(
        host = "sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False,
        old_style=True
    )
    # body containing search parameters for devices
    search_params= {
        "family": "Switches and Hubs",
        "type": "Cisco Catalyst 9300 Switch",
    }
    # request list of network devices that match the parameters
    devices = dnac.req("dna/intent/api/v1/network-device", params=search_params)

    device_uuids=[]

    # iterate over response data, print device UUID's and save them in list
    for dev in devices.json()["response"]:

        if not dev["errorCode"]:
            print(f"Adding {dev['hostname']}: {dev['instanceUuid']}")
            device_uuids.append(dev['instanceUuid'])

    # create body containing list of commands to execute and list of device UUID's you want to execute the commands on
    command_body = {
        "commands": ["show inventory", "show version", "show badstuff"],
        "deviceUuids": device_uuids,
    }

    # post the command payload
    run_resp = dnac.req(
        "dna/intent/api/v1/network-device-poller/cli/read-request",
        method="post",
        jsonbody=command_body
    )

    # wait for asynchronous operation to complete and get output file ID
    run_task = dnac.wait_for_task(run_resp.json()["response"]["taskId"])
    file_id = json.loads(run_task.json()["response"]["progress"]["fileId"])
    file_resp= dnac.req(f"dna/intent/api/v1/file/{file_id}")

    # create cmd_outputs directory
    file_dir=f"{Path.cwd()}/cmd_outputs"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # iterate over items in response, print output and write output to file in cmd_outputs directory
    for item in file_resp.json():
        uuid = item["deviceUuid"]

        for result, cmd_dict in item["commandResponses"].items():

            for cmd, output in cmd_dict.items():
                print(f"{uuid}: {cmd} -> {result}")


                cmd_u = cmd.replace(" ", "_")
                with open(f"{file_dir}/{uuid}_{cmd_u}.txt", "w") as handle:
                    handle.write(output)

if __name__=="__main__":
    main()
    