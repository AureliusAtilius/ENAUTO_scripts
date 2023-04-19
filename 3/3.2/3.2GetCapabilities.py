from ncclient import manager

router= {
        'host':'10.10.20.48',
        'port':'830',
        'username':'developer',
        'password':'C1sco12345',
}

with manager.connect(**router,hostkey_verify=False) as m:
        for capability in m.server_capabilities:
                print("*"*25)
                print(" ")
                print(capability)
                