import requests
import json

base_url = "https://sandbox-sdwan-2.cisco.com"
sess = requests.session()

def get_login(username, password):
    auth_url = f"{base_url}/j_security_check"

    login_body = {
        'j_username': username,
        'j_password': password
    }

    login_resp = sess.post(url=auth_url, data=login_body, verify=False)

    if login_resp.text:
        print("***** LOGIN FAILED *****")
        import sys
        sys.exit(1)
    else:
        print("***** LOGIN SUCCESS *****")
        return login_resp

token = get_login('devnetuser', 'RG!_Yw919_83')

def get_templates(url):
    template_urls = {
        't_list': f"{base_url}/dataservice/template/device",
        't_features': f"{base_url}/dataservice/template/feature",
        't_featuretypes': f"{base_url}/dataservice/template/feature/types"
    }

    template_resp = sess.get(url=template_urls[url], verify=False).json()
    print(template_resp)

get_templates('t_list')

def create_template():
    create_t_url = f"{base_url}/dataservice/template/device/feature"

    payload = {
       'templateName' : "<name>",
        'templateDescription' : "<description>",
        'deviceType' : "vmanage",
        'configType' : "template",
        'factoryDefault': False,
        'policyId' : "",
        'featureTemplateUidRange' : [],
        'generalTemplates': [
            {
                'templateId': "57b2rnfwf-3154-4354aab554",
                'templateType': "aaa"
            }
        ]
    }

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json"
    }

    response = sess.get(url=create_t_url, headers=headers, payload=payload, verify=False)
    print(json.dumps(response, indent=2))

# create_template()

template_id = '324543nv-g24a-2b4g-567jh2sd789agb'

def attach_template():
    device_temp_url = f"{base_url}/dataservice/template/device/config/input"

    device_template_payload = {
        'templateId': template_id,
        'deviceIds': ["34524724-vabf-g3m7-34c1-4356b6wec"],
        'isEdited': False,
        'isMasterEdited': False
    }

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json"
    }

    response = sess.post(url=device_temp_url, headers=headers, data=device_template_payload, verify=False).json()
    print(json.dumps(response, indent=2))
