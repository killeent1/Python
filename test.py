from jnpr.junos import Device
from jnpr.junos.exception import *
import csv
import json
from pprint import pprint
import multiprocessing
import time

'''constants'''
NUM_PROCESSES = 1
USER = "pyuser"
PASSWD = "PisaOy6be3zdhJPkLNm8"

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
def get_show_vlans(d,h):
    vlans_xml = d.rpc.get_vlan_information()
    vlans = vlans_xml.findall('.//l2ng-l2ald-vlan-instance-group')
    for vlan in vlans:
        vlan_dict = {}
        members_list = []
        vlan_dict['device'] = h
        vlan_dict['vlan_name'] = str(vlan.findtext('l2ng-l2rtb-vlan-name')).strip()
        vlan_dict['vlan_id'] = str(vlan.findtext('l2ng-l2rtb-vlan-tag')).strip()
        vlan_member = vlan.findall('l2ng-l2rtb-vlan-member')
        for member in vlan_member:
            x = str(member.findtext('l2ng-l2rtb-vlan-member-interface')).strip()
            members_list.append(x)
        vlan_dict['member_interfaces'] = members_list
        print(vlan_dict)

'''function for command: show vlans'''
def get_show_arp(d):
    arp_xml = d.rpc.get_arp_table_information()
    arp_table = arp_xml.findall('.//arp-table-entry')
    for arp in arp_table:
        arp_dict = {}
        arp_dict['mac'] = str(arp.findtext('mac-address')).strip()
        arp_dict['ip'] = str(arp.findtext('ip-address')).strip()
        arp_dict['interface_name'] = str(arp.findtext('interface-name')).strip()
        print(arp_dict)

'''function for command: show route'''
def get_show_interfaces(d,h):
    interface_list = []
    '''required for interface information from device'''
    interfaces_terse_xml = d.rpc.get_interface_information()
    '''required for hostname info'''
    interfaces = interfaces_terse_xml.findall('.//physical-interface')
    
    for i in interfaces:
        '''make new dictionary per row'''
        interface_dict = {}
        interface_dict['device'] = h
        interface_dict['name'] = str(i.findtext('name')).strip()
        interface_dict['admin_status'] = str(i.findtext('admin-status')).strip()
        interface_dict['oper_status'] = str(i.findtext('oper-status')).strip()
        interface_dict['description'] = str(i.findtext('description')).strip()
        interface_dict['speed'] = str(i.findtext('speed')).strip()
        #interface_dict['link_mode'] = str(i.findtext('link-mode')).strip()
        #interface_dict['link_level_type'] = str(i.findtext('link-level-type')).strip()
        '''add row to list'''
        interface_list.append(interface_dict)
    save_file(interface_list, h)
    
def get_software_info(d,h):
    version = d.facts['version']
    serial = d.facts['serialnumber']
    model = d.facts['model']
    print(f"{h},{version},{serial},{model}")
    

def save_file(my_list, h):
    csv_columns = my_list[0].keys()
    filename = h+"_marlow_vlans.csv"
    try:
        with open(filename, mode='w', newline='') as csv_file:
            file_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            file_writer.writeheader()
            for data in my_list:
                file_writer.writerow(data)
        print(f"\nSaved file: {filename}")
    except IOError as e:
        print(f"I/O Error: {e}")
    
    
def main():
    time_start = time.time()
    hosts = []
    '''open the hosts file for ssh access'''
    try:
        f = open("hosts.txt", "r")
        for x in f:
            hosts.append(x.rstrip())
        f.close()
    except FileNotFoundError:
        print("An exception occurred: File not found!")
    except:
        print("Something went wrong :( ")

    for ip_address in hosts:
        '''for each host in the list get facts'''
        try:
            dev = Device(host=ip_address, user=USER, passwd=PASSWD)
            dev.open()
            '''if connected ... run the functions'''
            if dev.connected:
                '''get the hostname of the device'''
                hostname = dev.facts['hostname']
                get_software_info(dev, hostname)
                #pprint(dev.facts)
                #get_show_route(dev)
                #get_show_vlans(dev, hostname)
                get_show_interfaces(dev, hostname)
                #get_show_arp(dev)
                '''close connection to the device once done'''
                dev.close()
        except ConnectRefusedError:
            print("%s: Error - Device connection refused!" % ip_address)
        except ConnectTimeoutError:
            print("%s: Error - Device connection timed out!" % ip_address)
        except ConnectAuthError as err:
            print(f"{err}: Error - Authentication failure for user {ip_address}")
            
    print("\nEnd of script: %f sec." % (time.time() - time_start))
    
if __name__ == "__main__":
    main()
    