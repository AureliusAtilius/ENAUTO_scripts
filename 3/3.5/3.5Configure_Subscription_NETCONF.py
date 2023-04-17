from ncclient import manager
import xmltodict
from lxml.etree import fromstring

router = {
    "host":"10.10.20.48",
    "port":"830",
    "username":"developer",
    "password":"C1sco12345",
    "hostkey_verify": False,
    "device_params": {"name": "csr"}
}

with manager.connect(**router) as m:
        # rpc = f"""
        #     <establish-subscription xmlns='urn:ietf:params:xml:ns:yang:ietf-event-notifications' xmlns:yp='urn:ietf:params:xml:ns:yang:ietf-yang-push'>
        #         <stream>yp:yang-push</stream>
        #         <yp:xpath-filter>/memory-ios-xe-oper:memory-statistics/memory-statistic</yp:xpath-filter>
        #         <yp:period>500</yp:period>
        #     </establish-subscription>
        # """


        rpc = """  
    <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
        <mdt-subscription>
            <subsciption-id> </subsciption-id>
            <base>
                <stream>yang-push</stream>
                <encoding>encode-kvgpb</encoding>
                <period>500</period>
                <xpath>/memory-ios-xe-oper:memory-statistics/memory-statistic</xpath>
            </base>
            <mdt-receivers>
                <address>10.10.20.50</address>
                <port>5236</port>
                <protocol>grpc-tcp</protocol>
            </mdt-receivers>
        </mdt-subscription>
    </mdt-config-data>"""
        response = m.dispatch(fromstring(rpc))
        python_resp = xmltodict.parse(response.xml)
        print(python_resp['rpc-reply']['subscription-result']['#text'])
        print(python_resp['rpc-reply']['subscription-id']['#text'])

        while True:
            sub_data = m.take_notification()
            python_sub_data = xmltodict.parse(sub_data.notification_xml)
            print(f"Sub ID: {python_sub_data['notification']['push-update']['subscription-id']}")
            print(python_sub_data)
            print(f"Name: {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['name']}")


