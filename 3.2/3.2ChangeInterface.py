from ncclient import manager
import xmltodict


router = {
    'host': "10.10.20.174",
    'port': "830",
    'user': "cisco",
    'password': "cisco"
}


int_conf = """
<filter>
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>GigabitEthernet2</name>
                <description>Port to Fabric</description>
                <enable>true</enabled>
            </interface>
        </interfaces>
    </config>
</filter>
"""


with manager.connect(**router, hostkey_verify=False) as m:
        response=m.edit_config(int_conf,target="running")
