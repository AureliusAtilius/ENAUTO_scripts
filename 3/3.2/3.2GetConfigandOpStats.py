from ncclient import manager
import xmltodict
router= {
        'host':'sandbox-iosxe-latest-1.cisco.com',
        'port':'830',
        'username':'admin',
        'password':'C1sco12345'
}


int_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
    </interfaces>
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
    </interfaces-state>
</filter>
"""

with manager.connect(**router, hostkey_verify=False) as m:
        netconf_response = m.get(int_filter)


python_response= xmltodict.parse(netconf_response.xml)['rpc-reply']['data']

print(python_response)

int_config= python_response['interfaces']['interface']
oper_state=python_response['interfaces-state']['interface']

'''
print("")
print(int_config)
print("")
print(oper_state)
'''
print(f"Name: {int_config['name']} {int_config['type']['#text']}")
print(F"Administrative Status: {oper_state['admin-status']} \nOperational Status: {oper_state['oper-status']} ")
