
from ncclient import manager
from lxml import etree as ET
from st2actions.runners.pythonrunner import Action

class NetconfDeviceConnection(Action):
    def run(self,ip_addr,username,password):
        netconf_conn = manager.connect(host=ip_addr, username=username, password=password,
    port=830, hostkey_verify=False, allow_agent=False, look_for_keys=False)

        custom_action = ET.Element("{http://tail-f.com/ns/netconf/actions/1.0}action",nsmap={'nca':"http://tail-f.com/ns/netconf/actions/1.0"})
        data_subelement = ET.SubElement(custom_action,"{http://tail-f.com/ns/netconf/actions/1.0}data")
        show_subelement = ET.SubElement(data_subelement,"show",xmlns="urn:brocade.com:mgmt:brocade-common-def")
        zoning_subelement = ET.SubElement(show_subelement,"zoning",xmlns="urn:brocade.com:mgmt:brocade-zone")
        
        print ET.tostring(custom_action,pretty_print=True)

#        uptime_element = ET.Element("get-system-uptime",xmlns="urn:brocade.com:mgmt:brocade-system")
#        print ET.tostring(uptime_element,pretty_print=True)

        try:
            rpc_data = netconf_conn.dispatch(custom_action)
            print rpc_data
        except Exception as Err:
            print("RPC Response Failure"),type(Err),Err
                     
        
#VDX = NetconfDeviceConnection('10.26.133.5', username='admin', password='password')


