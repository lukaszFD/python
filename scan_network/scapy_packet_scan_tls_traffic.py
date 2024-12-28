from scapy.layers.tls.all import TLS, TLSClientHello, TLSServerHello
from scapy.all import sniff, Raw
from scapy.layers.inet import IP, TCP
import re

# Mapowanie wersji TLS na tekstowe nazwy
TLS_VERSION_MAP = {
    0x0301: "TLS 1.0",   # 769
    0x0302: "TLS 1.1",   # 770
    0x0303: "TLS 1.2",   # 771
    0x0304: "TLS 1.3",   # 772
}


def analyze_tls(packet):
    """
    Analyze TLS packets for metadata and potential issues.
    """
    if packet.haslayer(TLS):
        tls_layer = packet[TLS]
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        tcp_port = packet[TCP].dport if packet[IP].src == ip_src else packet[TCP].sport

        print("\n[+] TLS Packet Detected:")
        print(f"Source IP: {ip_src}")
        print(f"Destination IP: {ip_dst}")
        print(f"Port: {tcp_port}")

        # Check for TLS Client Hello and extract SNI safely
        if tls_layer.haslayer(TLSClientHello):
            client_hello = tls_layer[TLSClientHello]

            # Log available fields
            print(f"Available Fields in ClientHello: {client_hello.fields}")

            if hasattr(client_hello, 'sni') and client_hello.sni:
                print(f"SNI (Server Name Indication): {client_hello.sni}")
            else:
                print("No SNI detected.")

            # Make sure we are getting the correct version
            if hasattr(client_hello, 'version'):
                print(f"TLS Version: {TLS_VERSION_MAP.get(client_hello.version, f'Unknown ({client_hello.version})')}")
            else:
                print("No TLS Version detected.")

            # Checking for cipher suites
            if hasattr(client_hello, 'ciphers'):
                print(f"Cipher Suites: {client_hello.ciphers}")
            else:
                print("No cipher suites detected.")

        print("-" * 50)


def extract_http_info(packet):
    """
    Extract HTTP method and endpoint from Raw data in the packet.
    """
    if packet.haslayer(Raw):
        try:
            raw_data = packet[Raw].load.decode(errors="ignore")
            # Sprawdzamy, czy dane zawierają linię HTTP (np. GET /index.html HTTP/1.1)
            match = re.match(r"(GET|POST|PUT|DELETE|PATCH)\s([^\s]+)\sHTTP/\d\.\d", raw_data)
            if match:
                method = match.group(1)  # GET, POST, PUT, itp.
                endpoint = match.group(2)  # Ścieżka (np. /index.html)
                return method, endpoint
        except Exception as e:
            print(f"Error extracting HTTP info: {e}")
    return None, None


def packet_callback(packet):
    """
    Callback function that processes each captured packet.
    """
    if packet.haslayer(TLS):
        try:
            # Sprawdzenie wersji TLS
            tls_version = packet[TLS].version
            tls_version_name = TLS_VERSION_MAP.get(tls_version, f"Unknown ({tls_version})")

            # Wyciągnięcie informacji HTTP (metoda, endpoint)
            method, endpoint = extract_http_info(packet)

            print(f"[+] TLS Packet Detected:")
            print(f"Source IP: {packet[IP].src}")
            print(f"Destination IP: {packet[IP].dst}")
            print(f"Port: {packet[TCP].sport if packet[IP].src == packet[IP].src else packet[TCP].dport}")
            print(f"TLS Version: {tls_version_name}")

            if method and endpoint:
                print(f"HTTP Method: {method}")
                print(f"HTTP Endpoint: {endpoint}")

            print("-" * 50)
        except Exception as e:
            print(f"Error processing TLS packet: {e}")

    # Analyzing TLS packets
    analyze_tls(packet)


if __name__ == "__main__":
    interface = 'Ethernet 3'

    print("Starting packet capture on port 443... Press Ctrl+C to stop.")

    try:
        sniff(iface=interface, prn=packet_callback, filter="tcp port 443", store=False)
    except KeyboardInterrupt:
        print("\nPacket capture stopped.")
