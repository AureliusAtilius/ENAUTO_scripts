import json,time,os
from pathlib import Path
from dnac_requester import DNACRequester


def main():
    
    # invoke instance of DNACRequester using DNAC sandbox 
    dnac= DNACRequester(
        host="sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False,
        old_style=True
    )
    
    # see if health outputs directory exists in current working directory, if not, create it
    health_dir=f"{Path.cwd()}\\health_outputs"
    if not os.path.exists(health_dir):
        os.makedirs(health_dir)
    
    # get current timestamp
    current_epoch = int(time.time() * 1000)
    params = {
        "timestamp": current_epoch
    }
    
    # create a request for each of the three types of health check containing timestamp
    for health in ["network", "site", "client"]:
        health_resp = dnac.req(
            f"dna/intent/api/v1/{health}-health",
            params=params,
        )

        # print response in human friendly format
        print(json.dumps(health_resp.json(),indent=2))

        # write response to a file in the health_outputs folder
        with open(f"{health_dir}\\get_{health}_health.json", "w") as handle:
            json.dump(health_resp.json(),handle,indent=2)
        print(f"Wrote {health} health to disk")


if __name__=="__main__":
    main()