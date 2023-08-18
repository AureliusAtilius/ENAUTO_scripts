import time,json
from dnac_requester import DNACRequester

def main():
    
    # invoke instance of DNACRequester using DNAC sandbox
    dnac = DNACRequester(
        host = "sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False,
        old_style=True
    )

    # request and print events
    events= dnac.req(f"dna/intent/api/v1/events", params={"tags": "ASSURANCE"})
    print(json.dumps(events.json(),indent=2))

    # get event ID's for each event in response
    event_ids= [event["eventId"] for event in events.json()]

    # json body containing payload for creating event webhook subscription
    body = [
        {
            "name": "globo_assurance",
            "subscriptionEndpoints": [
                {
                    "subscriptionDetails": {
                        "connectorType": "REST",
                        "name": "webhook.site",
                        "description": "great for testing",
                        "method": "POST",
                        "url": "https://webhook.site/dfff3fed-69fc-4309-8115-64d8a7f90080"
                    }
                }
            ],
            "filter": {"eventIDs": event_ids},
        }
    ]

    # post payload to create subscription
    add_resp= dnac.req(
        f"dna/intent/api/v1/event/subscription", method="post", jsonbody=body
    )

    # wait five seconds
    time.sleep(5)

    # request status of asynchronous operation
    add_status = dnac.req(add_resp.json()["statusUri"][1:]).json()

    if add_status["errorMessage"]:
        raise ValueError(add_status["statusMessage"])
    
    print(f"{add_status['statusMessage']} / {add_status['apiStatus']}")

    # request and print list of subscritptions to ensure it was created
    subs_resp = dnac.req(f"dna/intent/api/v1/event/subscription")

    print(json.dumps(subs_resp.json(),indent=2))







if __name__ =="__main__":
    main()