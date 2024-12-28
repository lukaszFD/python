import base64
import json
from scapy.all import sniff, Raw


def decode_basic_auth(header):
    """
    Decode Basic Auth credentials from the header.
    """
    try:
        encoded_creds = header.split(" ")[-1]  # Pobierz zakodowaną część
        decoded_creds = base64.b64decode(encoded_creds).decode("utf-8")
        username, password = decoded_creds.split(":", 1)
        return username, password
    except Exception as e:
        print(f"Error decoding Basic Auth: {e}")
        return None, None


def extract_post_body(raw_data):
    """
    Extract and format the body of a POST request as JSON.
    """
    try:
        body_start = raw_data.split("\r\n\r\n", 1)[-1]  # Treść body znajduje się za nagłówkami HTTP
        return json.dumps(json.loads(body_start), separators=(",", ":"))  # Formatuj jako JSON w jednej linii
    except Exception:
        return "Non-JSON body or empty"


def packet_callback(packet):
    """
    Callback function that processes each captured packet.
    """
    if packet.haslayer("IP") and packet.haslayer("TCP") and packet.haslayer(Raw):
        try:
            raw_data = packet[Raw].load.decode(errors="ignore")  # Dekoduj dane użytkownika

            # Wyszukaj Basic Auth w danych HTTP
            if "Authorization: Basic" in raw_data:
                print("\n[+] Basic Auth packet captured!")

                # Pobierz dane logowania
                username, password = decode_basic_auth(
                    next((line for line in raw_data.split("\r\n") if "Authorization: Basic" in line), "")
                )

                if username and password:
                    # Wyciągnij dane HTTP
                    ip_src = packet["IP"].src
                    ip_dst = packet["IP"].dst
                    tcp_port = packet["TCP"].dport if packet["IP"].src == ip_src else packet["TCP"].sport
                    host = next((line.split(": ", 1)[1] for line in raw_data.split("\r\n") if "Host:" in line),
                                "Unknown")
                    endpoint = next(
                        (line.split(" ")[1] for line in raw_data.split("\r\n") if line.startswith(("GET", "POST"))),
                        "Unknown")
                    http_method = raw_data.split(" ")[0]  # Typ żądania (GET, POST, itd.)

                    # Wyświetl informacje o pakiecie
                    print(f"Host: {host}")
                    print(f"Port: {tcp_port}")
                    print(f"Endpoint: {endpoint}")
                    print(f"HTTP Method: {http_method}")
                    print(f"Username: {username}")
                    print(f"Password: {password}")

                    # Dodatkowo dla POST: Wyświetl body w formacie JSON
                    if http_method == "POST":
                        post_body = extract_post_body(raw_data)
                        print(f"POST Body: {post_body}")

                    print("-" * 50)

        except Exception as e:
            print(f"Error processing packet: {e}")


if __name__ == "__main__":
    # Interfejs sieciowy do monitorowania (zmień w razie potrzeby)
    interface = 'Ethernet 3'

    print("Starting packet capture... Press Ctrl+C to stop.")

    # Uruchom przechwytywanie pakietów
    try:
        sniff(iface=interface, prn=packet_callback, filter="tcp", store=False)
    except KeyboardInterrupt:
        print("\nPacket capture stopped.")
