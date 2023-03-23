from ncclient import manager
from ncclient.xml_ import *

# device configs
switches = [
    {"host": "192.168.50.250", "port": "830", "username": "pyuser", "password": "PisaOy6be3zdhJPkLNm8"},
    {"host": "192.168.50.253", "port": "830", "username": "pyuser", "password": "PisaOy6be3zdhJPkLNm8"}
]

# loop through each switch and fetch data
for switch in switches:
    # make initial connection and save session as variable m
    with manager.connect(host=switch["host"], port=switch["port"], username=switch["username"], password=switch["password"], hostkey_verify=False, device_params={"name": "junos"}) as m:
        # get config in xml format
        response = m.get_configuration(format='xml')
        host = response.xpath('configuration/system/host-name')[0].text
        interfaces = response.xpath('configuration/interfaces/interface')
        print('*'*15)
        print(host)
        print('*'*15)
        
        for interface in interfaces:
            int_name = interface.xpath('name')[0].text
            int_unit = interface.xpath('unit/name')[0].text
            ip = []
            for name in interface.xpath('unit/family/inet/address/name'):
                print(f"{int_name}.{int_unit} {ip}")
                
print("\nend of script")