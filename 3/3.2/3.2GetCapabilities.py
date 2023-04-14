from ncclient import manager

router= {
        'host':'sandbox-iosxe-latest-1.cisco.com',
        'port':'830',
        'username':'admin',
        'password':'C1sco12345'
}

with manager.connect(**router,hostkey_verify=False) as m:
        for capability in m.server_capabilities:
                print("*"*25)
                print(" ")
                print(capability)
                