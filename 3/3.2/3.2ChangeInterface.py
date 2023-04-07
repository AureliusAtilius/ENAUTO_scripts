from ncclient import manager
import xmltodict
import xml.dom.minidom


router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "admin",
    'password': "C1sco12345"
}


int_conf = """
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>GigabitEthernet2</name>
                <description>Port to Fabric</description>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
"""


with manager.connect(**router, hostkey_verify=False) as m:
        response=m.edit_config(int_conf,target="running")
        xmlDom = xml.dom.minidom.parseString(str(response))
        print(xmlDom.toprettyxml( indent = "  " ))
