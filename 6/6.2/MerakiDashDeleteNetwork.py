import meraki
import json
from MerakiDashCreateNetwork import *


#use meraki always on sandbox. Disable logging.
merakiKey="fd6dd87d96915f21bc0e0b3d96a866ff0e53e381"
dashboard=meraki.DashboardAPI(merakiKey,suppress_logging=True)

#Get network ID 
def get_net_ID(network_list, network_name):
        for net in network_list:
                if net["name"]==network_name:
                        return net["id"]

#For deleting network by ID
def deleteNetwork(net_id):

        try:
                print("Removing Network")
                response=dashboard.networks.deleteNetwork(net_id)
                print(response)
        
        except Exception as ex:
                print(ex)

#For deleting the Organization
def deleteOrgs(org_id):
        try:
                print("Removing Organization")
                response=dashboard.organizations.deleteOrganization(org_id)
                print(response)
        except Exception as ex:
                print(ex)

if __name__=="__main__":
        #get org list
        org_list=get_orgs()
        
        #Get specific org ID
        org_name="Batman_Test_Org"
        org_id=get_org_ID(org_list=org_list, org_name=org_name)
        
        #Get network list
        network_list=get_networks(org_id=org_id)
        
        #Get specific network ID
        network_name="ENAUTO_Test"
        net_id=get_net_ID(network_list=network_list, network_name=network_name)
        
        #Check if specific network exists, if it does, delete it.
        if network_name not in str(network_list):
                print("Network not found.")
        else:
                deleteNetwork(net_id=net_id)

        #Check if specific organization exists, if it does, delete it.
        if org_id:
                deleteOrgs(org_id=org_id)
        else:
                print("Organization not found.")





