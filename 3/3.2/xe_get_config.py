from ncclient import manager
import xml.dom.minidom
import xmltodict

# Dictionary containing device info
router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "admin",
    'password': "C1sco12345"
}

# netconf filter in xml format for returning interface data for Loopback55
netconf_filter = '''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns = "urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Loopback55</name>
        </interface>
    </interfaces>
</filter>
'''

# Create netconf connection
with manager.connect(
        host= router['host'],
        port=router['port'],
        username=router['username'],
        password=router['password'],
        hostkey_verify= False
        ) as m:

        # get portion of running config specified by the filter
        netconf = m.get_config("running", netconf_filter) 

        # convert response to dictionary and store interface info in variable
        python_response= xmltodict.parse(netconf.xml)['rpc-reply']['data']
        int_config= python_response['interfaces']['interface']

        # print output
        print(f"Name: {int_config['name']} {int_config['type']['#text']}")
        print(f"IP Address: {int_config['ipv4']['address']['ip']} Netmask: {int_config['ipv4']['address']['netmask']}")

        print(xml.dom.minidom.parseString(netconf.xml).toprettyxml())