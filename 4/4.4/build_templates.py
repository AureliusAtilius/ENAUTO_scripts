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
    current_path=Path.cwd()
    for template in os.listdir(f"{current_path}/templates"):
        with open(f"{current_path}/templates/{template}", "r") as handle:
            temp_data= json.load(handle)

        print(f"\nCreating template from file {template}")
        temp_resp= dnac.req(
            f"dna/intent/api/v1/template-programmer/project/{'proj_id'}/template",
            method="post",
            jsonbody=temp_data["body"]
        )

        temp_task= dnac.wait_for_task(temp_resp.json()["response"]["taskId"])
        temp_id = temp_taks.json()["response"]["data"]


        prev_body = {"params": temp_data["params"], "templateId": temp_id}

        prev_data = dnac.req(
            "dna/intent/api/v1/template-programmer/template/preview",
            method="put",
            jsonbody=prev_body,
        ).json()

        print(f"Checking template {template}:")
        if prev_data["validationErrors"]:
            print(f"Errors:")
            for error in prev_data["validationErrors"]:
                print(f"{error['type']}: {error['message']}")

        else:
            print(f"Snippet rendered:")
            print(prev_data["cliPreview"])

            version_and_deploy(dnac, temp_data, temp_id)

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