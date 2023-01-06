from ncclient import manager
import xmltodict


router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "developer",
    'password': "C1sco12345"
}


int_conf = """
<filter>
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>GigabitEthernet2</name>
                <description>Port to Fabric</description>
                <enable>true</enable>
            </interface>
        </interfaces>
    </config>
</filter>
"""


with manager.connect(**router, hostkey_verify=False) as m:
        response=m.edit_config(int_conf,target="running")
