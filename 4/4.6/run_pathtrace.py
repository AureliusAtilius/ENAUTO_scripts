#!/usr/bin/env python

from dnac_requester import DNACRequester

def main():
    
    # invoke instance of DNACRequester using DNAC sandbox
    dnac = DNACRequester(
        host = "https://sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False
    )

    # create payload containing data needed to run pathtrace
    body = {
        "sourceIP": "10.10.20.81",
        "destIP": "10.10.20.82",
        "inclusions": ["INTERFACE-STATS", "DEVICE-STATS", "QOS-STATS"],
        "controlPath": False,
        "periodicRefresh": False,
    }

    # post request with payload
    path = dnac.req(
        "dna/intent/api/v1/flow-analysis", method="post", jsonbody=body
    )

    # get task ID of asynchronous operation and wait for completion
    path_data = path.json()["response"]
    task_resp = dnac.wait_for_task(path_data["taskId"])
    if task_resp.json()["respsonse"]["progress"] != path_data["flowAnalysisId"]:
        raise ValueError("Unexpected error; taask progress doesn't match flow id")
    
    # get results of pathtrace
    flow_resp = dnac.req(
        f"dna/intent/api/v1/flow-analysis/{path_data['flowAnalysisId']}"
    )

    # print results
    flow_data = flow_resp.json()["response"]
    print(
        f"Path trace {flow_data['request']['sourcIP']} -> "
        f"{flow_data['request']['destIP']}"
    )

    # print each hop in the pathtrace
    for i, hop in enumerate(flow_data["networkElementsInfo"]):
        print(f"Hop {i+1}: {hop['name']}")


if __name__=="__main__":
    main()