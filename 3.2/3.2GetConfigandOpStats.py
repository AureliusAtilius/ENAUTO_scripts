from ncclient import manager
import xmltodict
router= {
        'host':'ios-xe-mgmt-latest.com',
        'port':'830',
        'user':'developer',
        'password':'Cisco12345'
}


int_filter = """
<filter>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
    </interfaces>
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
    <interfaces-state>
</filter>
"""

with manager.connect(**router, hostkey_verify=False) as m:
        netconf_response = m.get(int_filter)


python_response= xmltodict.parse(netconf_response.xml)['rpc-reply']['data']


int_config= python_response['interfaces']['interface']
oper_state=python_response['interfaces-state']['interface']


print(f"Name: {int_config['name']['#text']}")
print("")
