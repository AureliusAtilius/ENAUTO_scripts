from ncclient import manager
import xmltodict
import xml.dom.minidom
router= {
        'host':'10.10.20.48',
        'port':'830',
        'username':'developer',
        'password':'C1sco12345'
}


int_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
        <mdt-subscription>
        </mdt-subscription>
      </mdt-config-data>
    </filter>
"""

with manager.connect(**router, hostkey_verify=False) as m:
        netconf_response = m.get(int_filter)


python_response= xmltodict.parse(netconf_response.xml)['rpc-reply']['data']

xmlDom = xml.dom.minidom.parseString(str(python_response))
print(xmlDom.toprettyxml( indent = "  " ))



