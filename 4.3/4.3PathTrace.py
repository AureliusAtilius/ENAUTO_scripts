import requests,argparse


def apic_login(host, username, password):
    """
    Use the REST API to Log into an APIC-EM and retrieve ticket
    """
    url = "https://{}/api/system/v1/auth/token".format(host)

    # Make Login request and return the response body
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password),
                                headers=headers, verify=False)˜

    # print the token
    print(response.text)

apic_login(apicem['host'], apicem['username'], apicem['password'])

parser = argparse.ArgumentParser()

# Command Line Parameters for Source and Destination IP
parser.add_argument("source_ip", help = "Source IP Address")
parser.add_argument("destination_ip", help = "Destination IP Address")
args = parser.parse_args()

# Get Source and Destination IPs from Command Line
source_ip = args.source_ip
destination_ip = args.destination_ip