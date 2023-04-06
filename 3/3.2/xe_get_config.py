from ncclient import manager
import xml.dom.minidom
import xmltodict
router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "admin",
    'password': "C1sco12345"
}

netconf_filter = '''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns = "urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Loopback55</name>
        </interface>
    </interfaces>
</filter>
'''

with manager.connect(
        host= router['host'],
        port=router['port'],
        username=router['username'],
        password=router['password'],
        hostkey_verify= False
        ) as m:

        netconf = m.get_config("running", netconf_filter) 

        python_response= xmltodict.parse(netconf.xml)['rpc-reply']['data']
        int_config= python_response['interfaces']['interface']

        print(f"Name: {int_config['name']} {int_config['type']['#text']}")
        print(f"IP Address: {int_config['ipv4']['address']['ip']} Netmask: {int_config['ipv4']['address']['netmask']}")

        print(xml.dom.minidom.parseString(netconf.xml).toprettyxml())