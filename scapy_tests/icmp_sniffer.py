from scapy.all import *
from scapy.layers.inet import ICMP


def packet_callback(packet):
    if ICMP in packet and packet[ICMP].type == 8: # Typ 8 to echo request ICMP print(f"Source: {packet[IP].src}, Load: {packet[ICMP].load}")

if name == "main": # Uruchomienie sniffing'u z filtrem ICMP typu echo request sniff(filter="icmp and icmp[0]=8", prn=packet_callback)