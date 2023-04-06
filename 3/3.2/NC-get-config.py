import sys
from ncclient import manager
import xml.dom.minidom

if __name__ == '__main__':
    router = {
    'host': "sandbox-iosxe-latest-1.cisco.com",
    'port': "830",
    'username': "admin",
    'password': "C1sco12345"
}

    m =  manager.connect(host=router['host'],
                         port=router['port'],
                         username=router['username'],
                         password=router['password'],
                         device_params={'name':"csr"})

    hostname_filter = '''
                      <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <hostname xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            </hostname>
                          </native>
                      </filter>
                      '''

       # Pretty print the XML reply
    xmlDom = xml.dom.minidom.parseString( str( m.get_config('running', hostname_filter)))
    print(xmlDom.toprettyxml( indent = "  " ))