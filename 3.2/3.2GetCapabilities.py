from ncclient import manager

router= {
        'host':'ios-xe-mgmt-latest.com',
        'port':'830',
        'user':'developer',
        'password':'Cisco12345'
}

with manager.connect(**router,host_key_verify=False) as m:
        for capability in m.server_capabilities:
                print("*"*25)
                print(" ")
                print(capability)
                