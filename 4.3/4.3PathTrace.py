import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import env_lab


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

token = get_token()

