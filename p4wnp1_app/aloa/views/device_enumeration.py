import os
import socket
import nmap

def enumerate_devices(network_subnet):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_subnet, arguments='-sn')
    devices = nm.all_hosts()
    return devices

def extract_device_details(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-O')
    if nm[ip].hostname():
        print('Hostname: %s' % nm[ip].hostname())
    if 'osmatch' in nm[ip]:
        for osmatch in nm[ip]['osmatch']:
            print('OS: %s' % osmatch['name'])

    nm.scan(ip, arguments='-p-')
    for proto in nm[ip].all_protocols():
        lport = nm[ip][proto].keys()
        for port in lport:
            print ('Port : %s\t State : %s' % (port, nm[ip][proto][port]['state']))

def device_enumeration(request):
    network_subnet = get_network_subnet()
    devices = enumerate_devices(network_subnet)
    for device in devices:
        print("Device IP: ", device)
        extract_device_details(device)
    return HttpResponse("Device enumeration complete")
