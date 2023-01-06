from ncclient import manager
import xml.dom.minidom
router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "developer",
    'password': "C1sco12345"
}

netconf_filter = '''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns = "urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>

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
        

        print(xml.dom.minidom.parseString(netconf.xml).toprettyxml())