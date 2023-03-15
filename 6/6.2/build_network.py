import os, json
from meraki_helpers import find_id_by_name, req
from pathlib import Path

def main(org_name):

    orgs = req("organizations").json()


    print(json.dumps(orgs, indent=2))

    org_id = find_id_by_name(orgs, org_name)

    if not org_id:
        raise ValueError(f"Could nt find organization {org_name}")
    

    print(f"Found {org_name} with ID {org_id}")

    cur_nets= req(f"organizations/{org_id}/networks").json()

    print(json.dumps(cur_nets,indent=2))

    with open(f"{Path.cwd()}\\6\\6.2\\add_networks.json", "r") as handle: 
        add_nets = json.load(handle)

        for item in add_nets:

            net_name = item["body"]["name"]
            net_id = find_id_by_name(cur_nets,net_name)

            if net_id:
                print(f"Network {net_name} already exists ({net_id})")
                continue
            new_net = req(
                f"/organizations/{org_id}/networks",
                method="post",
                jsonbody=item["body"],
            ).json()

            net_id = new_net["id"]
            print(f"Created network {net_name} with ID {net_id}")

            print(json.dumps(new_net, indent=2))

            for device in item["devices"]:
                req(
                    f"networks/{net_id}/devices/claim",
                    method="post",
                    jsonbody=device["add"],
                )
                sn = device["add"]["serial"]
                print(f"Device with SN {sn} added")

                update = req(
                    f"networks/{net_id}/devices/{sn}",
                    method="put",
                    jsonbody=device["update"],
                ).json()
                print(f"Device with SN {sn} named {device['update']['name']}")

                print(json.dumps(update, indent=2))


if __name__=="__main__":
    main("Gotham City Bank")
