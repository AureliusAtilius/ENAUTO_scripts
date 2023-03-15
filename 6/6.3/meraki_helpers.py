import os
import requests


def find_id_by_name(list_of_dicts, search_name):
    
    found_id = None
    
    for item in list_of_dicts:
        if item["name"].lower() == search_name.lower():
            found_id = item["id"]
            break
    return found_id

def get_network_id(net_name, org_name="devnet sandbox"):

    orgs= req("organizations").json()

    org_id = find_id_by_name(orgs,org_name)

    if not org_id:
        raise ValueError(f"Could not find {org_name} organization")
    
    nets = req(f"organization/{org_id}/networks").json()

    net_id= find_id_by_name(nets, net_name)

    if not net_id:
        raise ValueError(f"Could not find {net_name} network")
    
    return net_id


def req(resource, method="get", jsonbody=None, params=None):


    api_path="https://dashboard.meraki.com/api/v0"
    api_key = "fd6dd87d96915f21bc0e0b3d96a866ff0e53e381"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-Api-Key": api_key,
    }

    resp = requests.request(
        method=method,
        url = f"{api_path}/{resource}",
        headers=headers,
        json=jsonbody,
        params=params,
    )

    resp.rais_for_status()

    return resp
