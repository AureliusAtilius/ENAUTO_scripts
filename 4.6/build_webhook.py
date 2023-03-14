import time,json
from dnac_requester import DNACRequester

def main():
    
    dnac = DNACRequester(
        host = "sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False,
        old_style=True
    )

    events= dnac.req(f"dna/intent/api/v1/events", params={"tags": "ASSURANCE"})

    print(json.dumps(events.json(),indent=2))

    event_ids= [event["eventId"] for event in events.json()]

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

    add_resp= dnac.req(
        f"dna/intent/api/v1/event/subscription", method="post", jsonbody=body
    )

    time.sleep(5)

    add_status = dnac.req(add_resp.json()["statusUri"][1:]).json()

    if add_status["errorMessage"]:
        raise ValueError(add_status["statusMessage"])
    
    print(f"{add_status['statusMessage']} / {add_status['apiStatus']}")

    subs_resp = dnac.req(f"dna/intent/api/v1/event/subscription")

    my_sub = subs_resp.json()[-1]







if __name__ =="__main__":
    main()