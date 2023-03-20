#!/usr/bin/env python

import os,json,sys
from meraki_helpers import get_network_id



def main(org_name, net_name,file_name):

    net_id = get_network_id(net_name, org_name)

    with open(file_name, "r") as handle:
        portals = json.load(handle)

    for ssid_number, body in portals.items():

        ssid_base = f"networks/{net_id}/ssids/{ssid_number}"

        print(f"Updating SSID {ssid_number} for {body['ssid_body']['name']}")
        update_ssid = req(ssid_base, method="put", jsonbody=body["ssid_body"])


        if body["splash_body"]:

            f"Update SSID {ssid_number} excap "
            f"to {body['splash_body']['splashUrl']}"
            update_splash = req(
                f"{ssid_base}/splashSettings",
                method="put",
                jsonbody=body["splash_body"]
            )

if __name__=="__main__":
    
    org = os.environ.get("MERAKI_ORG_NAME", "Devnet Sandbox")

    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    if len(sys.argv) != 2:
        print("usage: python build_portals.py <path_to_json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    if not os.path.exists(json_file):
        print(f"file '{json_file}' does not exist")
        sys.exit(2)

    main(org, net, json_file)