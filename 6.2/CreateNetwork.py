import requests,json
from requests.exceptions import HTTPError
import meraki


#use meraki always on sandbox
merakiKey="fd6dd87d96915f21bc0e0b3d96a866ff0e53e381"
base_url="https://api.meraki.com/api/v1"

headers={
        'x-Cisco-Meraki-API-Key': merakiKey,
        'Accept':'application/json',
        'Content-Type':'application/json'
}

#get list of meraki orgs
def get_orgs():
        org_url=f"{base_url}/organizations"

        try:
                response=requests.get(url=org_url, headers=headers).json()
                #response=json.dumps(response, indent=2)
                return(response)
        except Exception as ex:
                print(ex)


#get list of meraki organization networks  
def get_networks(org_id):
        org_url=f"{base_url}/organizations/{org_id}/networks"

        try:
                response=requests.get(url=org_url, headers=headers).json()
                response=json.dumps(response, indent=2)
                return(response)
        except Exception as ex:
                print(ex)

#create meraki organization
def create_orgs():
        
        org_url=f"{base_url}/organizations"
        payload={
                "name": "Batman_Test_Org"
        }

        try:
                response=requests("POST",url=org_url, headers=headers,data=json.dumps(payload))
                return(response)
        except Exception as ex:
                print(ex)

#create meraki organization network
def create_network(org_id):
        network_url=f"{base_url}/organizations/{org_id}/networks"

        payload={
                "name":"ENAUTO_Test",
                "productTypes": [
                        "appliance",
                        "switch",
                        "wireless"
                ]
        }

        
        try:
                response = requests.post(url=network_url,headers=headers,data=json.dumps(payload))
                print(response.status_code)
                print(response.text)
        except Exception as ex:
                print(ex)

#check org list for specific organization name and return org id
def get_org_ID(org_list, org_name):
        
        for org in org_list:
                if org["name"]== org_name:
                        return org["id"]


if __name__=="__main__":

        #get org list
        org_list=get_orgs()

        #check for specific org and get id
        org_id=get_org_ID(org_list=org_list, org_name="Batman_Test_Org")
        print(org_id)

        #if specific org doesn't exist, create it
        if not org_id:
                create_orgs()
        
        #get network list
        network_list=get_networks(org_id=org_id)
        print(network_list)

        #check for specific network by name, if it doesn't exist, create it
        network_name='ENAUTO_Test'
        if network_name not in network_list:
                create_network(org_id=org_id)

        #get network list again to show newly created network
        network_list=get_networks(org_id=org_id)
        print(network_list)        
        
