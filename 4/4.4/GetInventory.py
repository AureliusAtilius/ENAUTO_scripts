import requests
from requests.exceptions import HTTPError
import json
from get_token import get_token

token=get_token()

headers = {
    'x-auth-token': token,
    'accept': "application/json",
    'content-type': "application/json"
}

def get_device_list():
        base_url = "https://sandboxdnac.cisco.com/dna"
        dev_list_url = f"{base_url}/intent/api/v1/network-device"

        try:
                get_list=requests.get(url=f"{dev_list_url}",headers=headers,verify=False).json()['response']
        except Exception as ex:
                print(f"Error has occurred: \n ---> {ex}")
        else:
                return get_list


if __name__=="__main__":
    token=get_token()

    headers = {
        'x-auth-token': token,
        'accept': "application/json",
        'content-type': "application/json"
    }

    dev_list_resp = get_device_list()
    print(json.dumps(dev_list_resp, indent=2))

