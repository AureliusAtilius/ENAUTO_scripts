import env_lab
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3

#Returns list of Command Runner CLI commands available for remote command execution.

# Disable the SSL warning on the DevNet Sandbox; never do this in production
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
urllib3.disable_warnings()

def get_token(host=env_lab.DNA_CENTER['host'],
              username=env_lab.DNA_CENTER['username'],
              password=env_lab.DNA_CENTER['password'],
              port=env_lab.DNA_CENTER['port']):
    """
    Use the REST API to log into an DNA_CENTER and retrieve a token
    """
    url = "https://{}:{}/dna/system/api/v1/auth/token".format(host,port)
    # Make Login request and return the response body
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), verify=False)
    token = response.json()["Token"]
    return token
  
  
def get_commands(token, host=env_lab.DNA_CENTER['host'], port=env_lab.DNA_CENTER['port']):
    url = "https://{}:{}/api/v1/network-device-poller/cli/legit-reads".format(host,port)
    headers = {
        "X-Auth-Token": token
        }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    print("Exec commands supported:")
    print(json.dumps(response.json()['response'], indent=4))

if __name__ == '__main__':

    get_commands(get_token())