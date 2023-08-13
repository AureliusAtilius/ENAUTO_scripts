from netmiko import ConnectHandler


# Dictionary containing device info
router = {
        'host':'sandbox-iosxe-latest-1.cisco.com',
        'port': '22',
        'username':'admin',
        'password':'C1sco12345',
        'device_type':'cisco_ios'
}

# List containing consecutive cli commands to be executed
configs=["int loopback55","ip address 10.101.75.1 255.255.255.0","no shut"]


# Attempt to connect to device and send commands
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