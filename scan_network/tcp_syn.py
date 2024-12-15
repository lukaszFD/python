from scapy.all import IP, TCP, sr1

# Wysyłanie pakietu TCP SYN do urządzenia Android
ip = "192.168.1.00"  # Adres IP urządzenia Android
syn_packet = IP(dst=ip) / TCP(dport=80, flags='S')
response = sr1(syn_packet)

if response:
    print("Odpowiedź od urządzenia:", response.show())
else:
    print("Brak odpowiedzi.")
