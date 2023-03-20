#!/usr/bin/env python

import os
from meraki_helpers import get_network_id

def main(org_name, net_name):

    net_id = get_network_id(net_name, org_name)

    get_clients = req(f"networks/{net_id}/clients").json()

    for i, client in enumerate(get_clients):
        print(
            f"{i+1}. Name: {client['description']} "
            f"MAC: {client['mac']} Status: {client['status']}"
        )



if __name__=="__main__":
    org = os.environ.get("MERAKI_ORG_NAME", "Devnet Sandbox")

    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    main(org,net)