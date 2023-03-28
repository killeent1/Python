from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import csv
import json
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
    for a in arp:
        mac = a.findtext('mac-address')
        ip = a.findtext('ip-address')
        print(f"{mac}{ip}")

'''function for command: show route'''
def get_show_interfaces(d):
    interface_list = []
    '''required for interface information from device'''
    interfaces_xml = d.rpc.get_interface_information(terse=True)
    '''required for hostname info'''
    system_info_xml = d.rpc.get_system_information()
    '''find all physical attributes of the interface and save as a list'''
    interfaces = interfaces_xml.findall('.//physical-interface')
    '''extract host-name from system info output'''
    system_info = str(system_info_xml.findtext('host-name')).strip()
    for i in interfaces:
        interface_dict = {}
        interface_dict['hostname'] = system_info
        interface_dict['name'] = str(i.findtext('name')).strip()
        interface_dict['admin_status'] = str(i.findtext('admin-status')).strip()
        interface_dict['oper_status'] = str(i.findtext('oper-status')).strip()
        interface_list.append(interface_dict)
        print(interface_list)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(interface_list, f, ensure_ascii=False, indent=4, sort_keys=True)
        print("saved file")
    save_file(interface_list, system_info)

def save_file(my_list, system_name):
    csv_columns = ['hostname','name','admin_status','oper_status']
    filename = system_name+"_marlow_connections.csv"
    try:
        with open(filename, mode='w') as csv_file:
            file_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            file_writer.writeheader()
            for data in my_list:
                file_writer.writerow(data)
        print("\nsaved file.")
    except IOError:
        print("I/O Error")
    

def main():
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
            if dev.connected:
                #pprint(dev.facts)
                #get_show_route(dev)
                #get_show_vlans(dev)
                get_show_interfaces(dev)
                print("\nFinished get_show_interfaces command")
                #get_show_arp(dev)
                '''close connection to the device'''
                dev.close()

        except ConnectError as err:
            print("Cannot connect to device: {0}".format(err))
        except Exception as err:
            print(err)
            
    print("\nEnd of script")
    
if __name__ == "__main__":
    main()
    