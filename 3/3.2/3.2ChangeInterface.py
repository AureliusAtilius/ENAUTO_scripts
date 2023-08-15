from ncclient import manager
import xmltodict
import xml.dom.minidom

# Dictionary containing device info
router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "admin",
    'password': "C1sco12345"
}

# xml netconf filter for editing state and description for GigabitEthernet2
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

# Attempt to connect to device
with manager.connect(**router, hostkey_verify=False) as m:
        # send netconf filter to the running config
        response=m.edit_config(int_conf,target="running")

        # return output in human readable format
        xmlDom = xml.dom.minidom.parseString(str(response))
        print(xmlDom.toprettyxml( indent = "  " ))
