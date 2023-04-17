from ncclient import manager
import xmltodict
router= {
        'host':'10.10.20.48',
        'port':'830',
        'username':'developer',
        'password':'C1sco12345'
}


int_filter = """
<filter>
      <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
        <mdt-subscription>
          <subscription-id>101</subscription-id>
          <base>
            <stream>yang-push</stream>
            <encoding>encode-kvgpb</encoding>
            <period>500</period>
            <xpath>/memory-ios-xe-oper:memory-statistics/memory-statistic</xpath>
          </base>
        </mdt-subscription>
      </mdt-config-data>
    </filter>
"""

with manager.connect(**router, hostkey_verify=False) as m:
        netconf_response = m.get(int_filter)


python_response= xmltodict.parse(netconf_response.xml)['rpc-reply']['data']

print(python_response)




