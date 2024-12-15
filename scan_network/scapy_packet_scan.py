from scapy.all import sniff

def packet_callback(packet):
    """
    Callback function that processes each captured packet.
    """
    # Sprawdź, czy pakiet ma warstwę IP
    if packet.haslayer("IP"):
        ip_src = packet["IP"].src  # Adres źródłowy
        ip_dst = packet["IP"].dst  # Adres docelowy

        # Filtruj pakiety według interesujących adresów IP
        if ip_src in {"192.168.1.35", "192.168.1.42"} or ip_dst in {"192.168.1.35", "192.168.1.42"}:
            print(f"Packet: {ip_src} -> {ip_dst}, Protocol: {packet['IP'].proto}, Size: {len(packet)} bytes")


if __name__ == "__main__":
    # Interfejs sieciowy do monitorowania (zmień w razie potrzeby)
    interface = 'WiFi'

    print("Starting packet capture... Press Ctrl+C to stop.")

    # Uruchom przechwytywanie pakietów
    try:
        sniff(iface=interface, prn=packet_callback, filter="ip", store=False)
    except KeyboardInterrupt:
        print("\nPacket capture stopped.")
