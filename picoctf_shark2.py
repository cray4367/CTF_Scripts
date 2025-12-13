# This is basically a script that extracts the source port from a given selection of ports on the source side using scapy
from scapy.all import *
flag=""
packets=rdpcap("capture.pcap")
for packet in packets:
	if UDP in packet and packet[UDP].dport==22:
		flag+=chr(packet[UDP].sport-5000)
print("Flag: {}".format(flag))
