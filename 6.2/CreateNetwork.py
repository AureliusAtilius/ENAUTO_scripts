import requests,json
from requests.exceptions import HTTPError

merakiKey="<key>"
base_url="https://api.meraki.com/api/v0"

headers={
        'x-Cisco-Meraki-API-Key': merakiKey,
        'Accept':'application/json',
        'Content-Type':'application/json'
}


def get_orgs():
        org_url=f"{base_url}/organizations"

        try:
                response=requests.get(url=org_url, headers=headers)
                return(response)
        except Exception as ex:
                print(ex)
        
orgs = get_orgs().json()
org_id="<orgId>"


def create_network(org_id):
        network_url=f"{base_url}/{org_id}/networks"

        payload={
                'name':'<name>',
                'type':'appliance switch camera'
        }
        try:
                response = requests.post(url=network_url,headers=headers,data=json.dumps(payload))
                if response.status_code==201:
                        print(response.text)
        except Exception as ex:
                print(ex)


create_network(org_id)

