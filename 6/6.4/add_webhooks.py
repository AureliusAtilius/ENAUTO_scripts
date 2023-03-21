
#!/usr/bin/env python
import os 
import time
import json
from meraki_helpers import get_network_id, req

def main(org_name, net_name):
    net_id = get_network_id(net_name, org_name)

    with open("add_webhooks.json", "r") as handle:

        webhooks = json.load(handle)

    for webhook in webhooks:

        print(f"adding webhook '{webhook['name']}'")
        if not webhook["url"].lower().startswith("https"):
            print(f" url is not 'https', skipping")
            continue

        add_http= req(
            f"networks/{net_id}/httpServers", method="post", jsonbody=webhook
        ).json()

    test_http = req(
        f"networks/{net_id}/httpServers/webhookTests",
        method="post",
        jsonbody={"url": webhook["url"]},
    ).json()

    if test_http["status"] != "enqueued":
        raise ValueError(f"webhook creation failed: {test_http['status']}")
    
    while test_http["status"] == "enqueued":
        time.sleep(2)
        test_http = req(
            f"networks/{net_id}/httpServers/webhookTests/{test_http['id']}",
        ).json()

    if test_http["status"] != "delivered":
        raise ValueError(f"webhook delivery failed: {test_http['status']}")
    
    net_http = req(f"networks/{net_id}/httpServers").json()
    print(f"Current webhook receivers for {net_name}:")
    print(json.dumps(net_http, indent=2))

if __name__=="__main__":

    org = os.environ.get("MERAKI_ORG_NAME", "Devnet Sandbox")

    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    main(org,net)

