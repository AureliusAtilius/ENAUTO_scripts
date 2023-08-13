from ncclient import manager
import xmltodict
import xml.dom.minidom

# dictionary containing device connection info
router= {
        'host':'10.10.20.48',
        'port':'830',
        'username':'developer',
        'password':'C1sco12345'
}

# NETCONF filter in xml format requesting all mdt subscriptions
int_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
        <mdt-subscription>
        </mdt-subscription>
      </mdt-config-data>
    </filter>
"""
# connect to device and request data specified in filter
with manager.connect(**router, hostkey_verify=False) as m:
        netconf_response = m.get(int_filter)

# convert response to human friendly format and print
xmlDom = xml.dom.minidom.parseString(str(netconf_response))
print(xmlDom.toprettyxml( indent = "  " ))



