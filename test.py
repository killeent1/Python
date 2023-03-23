import sys
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from getpass import getpass
from pprint import pprint

#hostname = input("Device hostname: ")
#junos_username = input("JUNOS username: ")
junos_username = "tkilleen"
hosts = []

'''open the hosts file for ssh access'''
try:
    f = open("hosts.txt", "r")
    for x in f:
        print(x)
        hosts.append(x.rstrip())
    f.close()
except FileNotFoundError:
    print("An exception occurred: File not found!")

for h in hosts:
    junos_password = getpass("Password for : {}\n".format(h))
    try:
        dev = Device(host=h, user=junos_username, passwd=junos_password)
        dev.open()
        print(dev.connected)
        pprint(dev.facts)
        
        dev.close()
        print(dev.connected)
    
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        sys.exit(1)
    except Exception as err:
        print(err)
        sys.exit(1)

print("end of script")