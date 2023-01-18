import meraki
import json

#use meraki always on sandbox
merakiKey="fd6dd87d96915f21bc0e0b3d96a866ff0e53e381"


def get_orgs():
        dashboard= meraki.DashboardAPI(merakiKey,suppress_logging=True)
        response= dashboard.organizations.getOrganizations()
        return response

def get_org_ID(org_list, org_name):
        for org in org_list:
                if org["name"]== org_name:
                        return org["id"]

def create_orgs(org_name):
        dashboard= meraki.DashboardAPI(merakiKey,suppress_logging=True)
        name = org_name
        try:

                response = dashboard.organizations.createOrganization(name)
                return response
        except Exception as ex:
                print(ex)

def get_networks(org_id):
        organization_id=org_id
        dashboard=meraki.DashboardAPI(merakiKey,suppress_logging=True)

        try:
                response=dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')
                return response
        except Exception as ex:
                print(ex)

def create_network(org_id,network_name):
        dashboard=meraki.DashboardAPI(merakiKey,suppress_logging=True)
        product_types= ['appliance','switch','camera']

        try:
                response=dashboard.organizations.createOrganizationNetwork(
                        organizationId=org_id,
                        name=network_name,
                        productTypes=product_types,
                        tags=['tag1','tag2',],
                        timeZone='America/Los_Angeles',
                        notes='Combined network for Long Island Office')
                return response

        except Exception as ex:
                print(ex)
if __name__=="__main__":
        #get org list
        org_list=get_orgs()

        #check for specific org and get id
        org_id=get_org_ID(org_list=org_list, org_name="Batman_Test_Org")
        print(org_id)

        #if specific org doesn't exist, create it
        if not org_id:
                create_orgs("Batman_Test_Org")
        else:
                print("Organization already exists.")
        
        #get network list
        network_list=get_networks(org_id=org_id)
        print(network_list)

        #check for specific network by name, if it doesn't exist, create it
        network_name='ENAUTO_Test'
        if network_name not in json.dumps(network_list, indent=2):
                create_network(org_id=org_id,network_name="ENAUTO_Test")
        else:
                print("Network already exists.")

        #get network list again to show newly created network
        network_list=get_networks(org_id=org_id)
        print(network_list)