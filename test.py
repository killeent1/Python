from jnpr.junos import Device
from pprint import pprint

dev = Device(host='10.0.1.253', user='tkilleen', password='Cog@Lg1FGAVH:^T/%0g9')

dev.open()
print(dev.connected)
pprint(dev.facts)

dev.close()
print(dev.connected)