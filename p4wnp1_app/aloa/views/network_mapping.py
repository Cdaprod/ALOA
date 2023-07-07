# Aloa/views/network_mapping.py
import matplotlib.pyplot as plt
import socket
import scapy.all as scapy
import networkx as nx
import subprocess
import re
from django.http import HttpResponse

def get_network_subnet():
    try:
        result = subprocess.check_output("ip -o -f inet addr show | awk '/scope global/ {print $4}'", shell=True).decode('utf-8')
        subnets = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', result)
        return subnets[0] 
    except subprocess.CalledProcessError:
        print('There was an error running the subnet detection command.')
        return '127.0.0.1/8'
    except IndexError:
        print('Could not detect a valid subnet.')
        return '127.0.0.1/8'

def create_network_map():
    network_subnet = get_network_subnet()
    arp_request = scapy.ARP(pdst=network_subnet)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    try:
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    except PermissionError:
        print('Insufficient permissions to perform network scan. Please run the script with sudo privileges.')
        return []
    
    network_map = []
    
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        network_map.append(client_dict)
    return network_map

def visualize_network():
    try:
        network_map = create_network_map()
        G = nx.Graph()

        for node in network_map:
            G.add_node(node['ip'])

        nx.draw(G, with_labels = True)
        plt.savefig("NetworkMap.png")  # Saves the network map as NetworkMap.png
        return HttpResponse("Network mapping visualization created")
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse("An error occurred while visualizing the network")
