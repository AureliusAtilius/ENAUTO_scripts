import requests
from requests.exceptions import HTTPError
import time
import json
from get_token import get_token



def get_credentials(base_url, headers):
        cred_url = f"{base_url}/intent/api/v1/global-credential/cli"
        credentials = {
        'description': 'DNA Center Credentials',
        'enablePassword': '<pwd>',
        'password': '<pwd>',
        'username': '<user>',
        'credentialType': 'GLOBAL'
        }
        try:
                task_id_att = requests.post(url=f"{cred_url}", headers=headers, json=credentials, verify=False)
        except Exception as ex:
                print(f"Error has occurred: \n ---> {ex}")
        else:
                task_id = task_id_att.json()
                task_id_url = f"{base_url}/intent/api/v1/task/{task_id}"
                time.sleep(5)
        try:

                cred_att = requests.get(url=f"{task_id_url}", headers=headers, verify=False)
        except Exception as ex:
                print(f"Error has occurred: \n ---> {ex}")
        else:
                creds = cred_att.json()['progress']
                print("*** Credentials acquired ***")
        return creds

def begin_discovery(cred_id):
        discovery_url = f"{base_url}/intent/api/v1/discovery"
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
        try:
                task_id_att = requests.post(url=f"{discovery_url}", headers=headers, json=discovery, verify=False)
        except Exception as ex:
                print(f"Error occurred: \n ---> {ex}")
        else:
                task_id = task_id_att.json()['response']['taskId']
                time.sleep(10)
        try:
                discovery_att = requests.get(url=f"{task_id}", headers=headers, verify=False)
        except Exception as ex:
                print(f"Error occurred: \n ---> {ex}")
        else:
                discovery_id = discovery_att.json()['progress']
        return discovery_id


if __name__=="__main__":
        dna_token = get_token()
        # print(get_token())
        headers = {
        "x-auth-token": dna_token,
        "Accept": "application/json",
        "Content-type": "application/json"
        }
        base_url = "https://sandboxdnac.cisco.com/dna"
        cred_id = get_credentials(base_url=base_url, headers=headers)
        disc_id = begin_discovery(cred_id=cred_id)
        # print(disc_id_url)

        disc_devices_url = f"{base_url}/intent/api/v1/dsicovery/{disc_id}/network-device"
        dev_resp = requests.get(url=f"{disc_devices_url}")
        device_ips = []
        for device in dev_resp.json()['response']:
                device_ips.append({'ip': device['managementIpAddress']})
        print(device_ips)
