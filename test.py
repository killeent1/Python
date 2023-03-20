import sys
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from getpass import getpass
from pprint import pprint


hostname = input("Device hostname: ")
junos_username = input("JUNOS username: ")
junos_password = getpass("JUNOS or SSH key password: ")

#dev = Device(host='10.0.1.253', user='tkilleen', password='Cog@Lg1FGAVH:^T/%0g9')
dev = Device(host=hostname, user=junos_username, passwd=junos_password)

try:
    dev.open()
    print(dev.connected)
except ConnectError as err:
    print("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print(err)
    sys.exit(1)

pprint(dev.facts)
dev.close()
print(dev.connected)