from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from getpass import getpass
from pprint import pprint

'''variables'''
junos_username = "pyuser"
junos_password = "PisaOy6be3zdhJPkLNm8"
hosts = []

'''function for command: show route'''
def get_show_route(d):
    routes_xml = d.rpc.get_route_information(table='inet.0')
    routes = routes_xml.findall('.//rt')
    for route in routes:
        if route.findtext('rt-entry/protocol-name') != 'Local':
            dest = route.findtext('rt-destination')
            via = route.findtext('rt-entry/nh/via')
            print(f"{dest} via {via}")
            
'''function for command: show vlans'''
def get_show_vlans(d):
    vlans_xml = d.rpc.get_vlan_information()
    vlans = vlans_xml.findall('.//l2ng-l2ald-vlan-instance-group')
    for vlan in vlans:
        v = vlan.findtext('l2ng-l2rtb-vlan-name')
        t = vlan.findtext('l2ng-l2rtb-vlan-tag')
        print(f"{v} vlan {t}")

'''function for command: show vlans'''
def get_show_arp(d):
    arp_xml = d.rpc.get_arp_table_information()
    arp = arp_xml.findall('.//arp-table-entry')
    table = []
    for a in arp:
        mac = a.findtext('mac-address')
        ip = a.findtext('ip-address')
        print(f"{mac}{ip}")

'''function for command: show route'''
def get_show_interfaces(d):
    interface_dict = {}
    interfaces_xml = d.rpc.get_interface_information()
    system_info_xml = d.rpc.get_system_information()
    interfaces = interfaces_xml.findall('.//physical-interface')
    system_info = system_info_xml.findtext('host-name')
    print(system_info)l
    for i in interfaces:
        interface_dict['name'] = str(i.findtext('name')).strip()
        interface_dict['oper_status'] = str(i.findtext('oper-status')).strip()
        interface_dict['desc'] = str(i.findtext('description')).strip()
        print(interface_dict)

'''TODO
get interface information: type'''

'''open the hosts file for ssh access'''
try:
    f = open("hosts.txt", "r")
    for x in f:
        hosts.append(x.rstrip())
    f.close()
except FileNotFoundError:
    print("An exception occurred: File not found!")

for h in hosts:
    '''for each host in the list get facts'''
    try:
        dev = Device(host=h, user=junos_username, passwd=junos_password)
        dev.open()
        print(dev.connected)
        #pprint(dev.facts)
        #get_show_route(dev)
        #get_show_vlans(dev)
        get_show_interfaces(dev)
        #get_show_arp(dev)
        
        '''close connection to the device'''
        dev.close()
        print(dev.connected)
    
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
    except Exception as err:
        print(err)

print("end of script")