import requests
from requests.exceptions import HTTPError
import time
import json
from get_token import get_token

# Script for starting a discovery of network devices.



# function for obtaining credentials needed to run discovery
def get_credentials(base_url, headers):
        # URL for global credential
        cred_url = f"{base_url}/intent/api/v1/global-credential/cli"
        
        # dictionary containing credential payload. Substitute your info <here>
        credentials = {
        'description': 'DNA Center Credentials',
        'enablePassword': '<pwd>',
        'password': '<pwd>',
        'username': '<user>',
        'credentialType': 'GLOBAL'
        }

        # attempt to post credential payload. If successful, response contains a task ID for asynchronous operation. Wait 5 seconds for task to complete
        try:
                task_id_att = requests.post(url=f"{cred_url}", headers=headers, json=credentials, verify=False)
        except Exception as ex:
                print(f"Error has occurred: \n ---> {ex}")
        else:
                task_id = task_id_att.json()
                task_id_url = f"{base_url}/intent/api/v1/task/{task_id}"
                time.sleep(5)
        
        # attempt to request task response from credential post
        try:
                cred_att = requests.get(url=f"{task_id_url}", headers=headers, verify=False)
        except Exception as ex:
                print(f"Error has occurred: \n ---> {ex}")
        else:
                creds = cred_att.json()['progress']
                print("*** Credentials acquired ***")
        return creds


# function for starting discovery
def begin_discovery(cred_id):
        # URL for discovery
        discovery_url = f"{base_url}/intent/api/v1/discovery"
        
        # dictionary containing payload with discovery info
        discovery = {
        "name": "Discovery-Guide",
        "discoveryType": "Range",
        "ipAddressList": "10.255.3.11-10.255.3.19",
        "protocolOrder": "ssh",
        "timeOut": 5,
        "retryCount": 3,
        "isAutoCdp": False,
        "globalCredentialIdList":cred_id
        }

        # attempt to post the discovery payload to start discovery
        try:
                task_id_att = requests.post(url=f"{discovery_url}", headers=headers, json=discovery, verify=False)
        except Exception as ex:
                print(f"Error occurred: \n ---> {ex}")
        else:
                # wait 10 seconds for task to complete
                task_id = task_id_att.json()['response']['taskId']
                time.sleep(10)
        
        # attempt to request task response
        try:
                discovery_att = requests.get(url=f"{task_id}", headers=headers, verify=False)
        except Exception as ex:
                print(f"Error occurred: \n ---> {ex}")
        else:
                discovery_id = discovery_att.json()['progress']
        return discovery_id


if __name__=="__main__":
        
        # get auth token
        dna_token = get_token()
        
        # REST API headers containing auth token
        headers = {
        "x-auth-token": dna_token,
        "Accept": "application/json",
        "Content-type": "application/json"
        }

        # base URL for DNAC sandbox
        base_url = "https://sandboxdnac.cisco.com/dna"

        # get credentials
        cred_id = get_credentials(base_url=base_url, headers=headers)

        # start discovery
        disc_id = begin_discovery(cred_id=cred_id)
        
        # request discovered devices using discovery ID 
        disc_devices_url = f"{base_url}/intent/api/v1/dsicovery/{disc_id}/network-device"
        dev_resp = requests.get(url=f"{disc_devices_url}")
        
        # iterate over response data and print list of device IP addresses
        device_ips = []
        for device in dev_resp.json()['response']:
                device_ips.append({'ip': device['managementIpAddress']})
        print(device_ips)
