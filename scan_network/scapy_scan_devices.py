from scapy.all import ARP, Ether, srp

def scan_network(ip_ranges, timeout=5):
    """
    Scans the specified network ranges for devices.

    Args:
        ip_ranges (list): List of IP ranges to scan (e.g., ['192.168.1.0/24', '192.168.56.0/24']).
        timeout (int): Timeout for ARP requests in seconds.

    Returns:
        list: List of devices with IP and MAC addresses.
    """
    devices = []

    for ip_range in ip_ranges:
        print(f"Scanning range: {ip_range}")
        # Create an ARP request packet
        arp_request = ARP(pdst=ip_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request

        # Send the packet and receive the responses
        answered_list = srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]

        for sent, received in answered_list:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


if __name__ == "__main__":
    import os

    # Define the IP ranges
    ip_ranges = ["192.168.56.0/24", "192.168.1.0/24"]
    print(f"Scanning networks: {', '.join(ip_ranges)}")

    # Scan the networks
    devices = scan_network(ip_ranges, timeout=5)

    # Display the results
    if devices:
        print("\nDevices found:")
        print("IP Address\t\tMAC Address")
        print("-" * 40)
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")
    else:
        print("No devices found.")

    # Optionally display the local ARP cache
    print("\nLocal ARP Cache:")
    os.system("arp -a")
