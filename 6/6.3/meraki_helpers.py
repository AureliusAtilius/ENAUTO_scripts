import os
import requests

# function that searches for a name in a list of dictionaries
def find_id_by_name(list_of_dicts, search_name):
    
    found_id = None
    
    for item in list_of_dicts:
        if item["name"].lower() == search_name.lower():
            found_id = item["id"]
            break
    return found_id

# function for requesting a network ID from Meraki Dashboard API
def get_network_id(net_name, org_name="devnet sandbox"):

    # send request for list of organizations
    orgs= req("organizations").json()

    # iterate over response to find ID
    org_id = find_id_by_name(orgs,org_name)

    # raise error if no ID could be found
    if not org_id:
        raise ValueError(f"Could not find {org_name} organization")
    
    # request list of networks in org using org ID
    nets = req(f"organization/{org_id}/networks").json()

    # find network ID by network name
    net_id= find_id_by_name(nets, net_name)

    # if no network found, return error
    if not net_id:
        raise ValueError(f"Could not find {net_name} network")
    
    return net_id

# function that connects to the Meraki dashboard and submits an API request
def req(resource, method="get", jsonbody=None, params=None):

    # Dashboard URL
    api_path="https://dashboard.meraki.com/api/v0"
    
    # Provide your own API key or use the sandbox
    api_key = "fd6dd87d96915f21bc0e0b3d96a866ff0e53e381"

    # API headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-Api-Key": api_key,
    }

    # send request
    resp = requests.request(
        method=method,
        url = f"{api_path}/{resource}",
        headers=headers,
        json=jsonbody,
        params=params,
    )

    resp.raise_for_status()

    return resp
