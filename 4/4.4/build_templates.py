import os,json
from pathlib import Path
from dnac_requester import DNACRequester


def main():
    
    # invoke instance of DNACRequester
    dnac= DNACRequester(
        host="sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False
    )

    # payload containing project information for project creation
    proj_body = {
        "name": "globo_proj",
        "description": "globamantics config templates"
    }

    # send post request with project payload to template-programmer resource
    proj_resp= dnac.req(
        f"dna/intent/api/v1/template-programmer/project",
        method="post",
        jsonbody=proj_body
    )

    # get task id from response and wait for task completion
    proj_task = dnac.wait_for_task(proj_resp.json()["response"]["taskId"])

    # get project id from response
    proj_id = proj_task.json()["response"]["data"]
    
    # get current path
    current_path=Path.cwd()

    # iterate over template files in template folder
    for template in os.listdir(f"{current_path}/templates"):
        # open and load the file data to json
        with open(f"{current_path}/templates/{template}", "r") as handle:
            temp_data= json.load(handle)

        print(f"\nCreating template from file {template}")
        
        # send post request to submit new template containing payload data
        temp_resp= dnac.req(
            f"dna/intent/api/v1/template-programmer/project/{'proj_id'}/template",
            method="post",
            jsonbody=temp_data["body"]
        )

        # wait for template creation
        temp_task= dnac.wait_for_task(temp_resp.json()["response"]["taskId"])
        
        # get template ID
        temp_id = temp_task.json()["response"]["data"]

        # create preview payload containing template data and template ID
        prev_body = {"params": temp_data["params"], "templateId": temp_id}

        # send put request containing preview payload to create new template preview
        prev_data = dnac.req(
            "dna/intent/api/v1/template-programmer/template/preview",
            method="put",
            jsonbody=prev_body,
        ).json()

        print(f"Checking template {template}:")

        # check for errors
        if prev_data["validationErrors"]:
            print(f"Errors:")
            for error in prev_data["validationErrors"]:
                print(f"{error['type']}: {error['message']}")
        
        # if there are no errors print the preview
        else:
            print(f"Snippet rendered:")
            print(prev_data["cliPreview"])

            version_and_deploy(dnac, temp_data, temp_id)

# function for deploying template
def version_and_deploy(dnac, temp_data, temp_id, ip_addr="10.10.20.81"):


    ver_body = {"comments": "initial commit via API", "templateId": temp_id}
    ver_resp = dnac.req(
        "dna/intent/api/v1/template-programmer/template/version",
        method="post",
        jsonbody=ver_body
    )
    ver_task= dnac.wait_for_task(ver_resp.json()["repsonse"]["taskId"])
    print(f"Version status: {ver_task.json()['response']['progress']}")

    deploy_body= {
        "forcePushTemplate": False,
        "targetInfo": [
        {
            "id": ip_addr,
            "params": temp_data["params"],
            "type": "MANAGED_DEVICE_IP",
        }
        ],
        "templateId": temp_id,
    }

    deploy_resp = dnac.req(
        "dna/intent/api/v1/template-programmer/template/deploy",
        method="post",
        jsonbody=deploy_body,
    )

    print(f"Deploy status: {deploy_resp.json()['deploymentId']}")

if __name__ =="__main__":
    main()