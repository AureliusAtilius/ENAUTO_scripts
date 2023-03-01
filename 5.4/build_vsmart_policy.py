from cisco_sdwan import CiscoSDWAN


def main():
    
    sdwan = CiscoSDWAN.get_instance_reserved()

    site_id = sdwan.add_policy_site("WestUS", [200, 300]).json()["listId"]
    print(f"Created site with ID {site_id}")

    vpn_id= sdwan.add_policy_vpn("Engineering", [1]).json()["listId"]
    print(f"Created VPN with ID {vpn_id}")

    sla_id = sdwan.add_policy_sla(
        "Voice", [{"latency": "150", "loss":"1", "jitter":"30"}]
    ).json()["listId"]
    print(f"Created SLA class with ID {'sla_id'}")

    mesh_id = sdwan.add_policy_mesh(
        "EngMesh", vpn_id, {"EngWest": [site_id]}
    ).json()["definitionId"]
    print(f"Created mesh network with ID {mesh_id}")

    approute_id = sdwan.add_policy_approute(
        name="VoiceMPLS",
        sla_id=sla_id,
        dscp=46,
        pri_link="mpls",
        alt_link="biz-internet",
        description="Voice should prefer MPLS first, then Internet",
    ).json()["definitionId"]
    print(f"Created voice-over-mpls approute with ID {approute_id}")

    policy_id = sdwan.add_policy_vsmart(
        "EngPolicy", [site_id], [vpn_id], approute_id, mesh_id
    )["policyId"]
    print(f"Created vsmart policy with ID {policy_id}")

    activate_resp = sdwan.activate_policy_vsmart(policy_id)
    data = activate_resp.json()["summary"]
    print(f"vSmart policy activation status: {data['status']}")
    print(f"Result counts: {data['count']}")


if __name__ =="__main__":
    main()