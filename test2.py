from ncclient import manager
from ncclient.xml_ import *

# device configs
switches = [
    {"host": "192.168.170.1", "port": "830", "password": "PisaOy6be3zdhJPkLNm8"},
    {"host": "192.168.170.2", "port": "830", "password": "PisaOy6be3zdhJPkLNm8"}
]

# loop through each switch and fetch data
for switch in switches:
    # make initial connection and save session as variable m
    with manager.connect(host=switch["host"], port=switch["port"], username="pyuser", password=switch["password"], hostkey_verify=False, device_params={"name": "junos"}) as m:
        # get config in xml format
        response = m.get_configuration(format='xml')
        host = response.xpath('configuration/system/host-name')[0].text
        interfaces = response.xpath('configuration/interfaces/interface')
        print('*'*15)
        print(host)
        print('*'*15)
        
        for interface in interfaces:
            int_name = interface.xpath('name')[0].text
            op_status = interface.xpath('physical-interface/oper-status')[0].text
            ip = []
            for name in interface.xpath('unit/family/inet/address/name'):
                ip.append(name.text)
            print(f"{int_name} {op_status} {ip}")
                
print("\nend of script")