from ncclient import manager
import xmltodict
from lxml.etree import fromstring

# dictionary containing device connection info
router = {
    "host":"10.10.20.48",
    "port":"830",
    "username":"developer",
    "password":"C1sco12345",
    "hostkey_verify": False,
    "device_params": {"name": "csr"}
}

# connect to device
with manager.connect(**router) as m:

        # NETCONF payload in xml format containing subscription mdt subscription info
        rpc = """
            <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
                <mdt-subscription>
                <subscription-id>101</subscription-id>
                <base>
                    <stream>yang-push</stream>
                    <encoding>encode-kvgpb</encoding>
                    <period>500</period>
                    <xpath>/memory-ios-xe-oper:memory-statistics/memory-statistic</xpath>
                </base>
                <mdt-receivers>
                    <address>10.10.20.50</address>
                    <port>5723</port>
                    <protocol>grpc-tcp</protocol>
                </mdt-receivers>
                </mdt-subscription>
            </mdt-config-data>
            </config>
            """
        # send request with payload to running configuration
        response = m.edit_config(rpc,target="running")

        # convert response to human friendly format and print
        python_resp = xmltodict.parse(response.xml)
        print(python_resp['rpc-reply'])

        