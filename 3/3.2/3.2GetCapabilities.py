from ncclient import manager

# dictionary containing device info
router= {
        'host':'10.10.20.48',
        'port':'830',
        'username':'developer',
        'password':'C1sco12345',
}

# attempt to connect to device
with manager.connect(**router,hostkey_verify=False) as m:
        # print the server capabilities
        for capability in m.server_capabilities:
                print("*"*25)
                print(" ")
                print(capability)
                