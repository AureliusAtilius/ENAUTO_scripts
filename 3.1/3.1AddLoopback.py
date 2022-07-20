from netmiko import ConnectHandler

router = {
        'host':'ios-xe-mgmt-latest.cisco.com',
        'port': '8181',
        'username':'root',
        'password':'Cisco12345',
        'device_type':'cisco_ios'
}

configs=["int loopback55","ip address 10.101.75.1 255.255.255.0","no shut"]


try:
        c=ConnectHandler(**router)
        c.enable()
        c.send_config_set(configs)
        response=c.send_command("show ip int brief")
        c.disconnect()

except Exception as ex:
        print(ex)

else:
        print(response)