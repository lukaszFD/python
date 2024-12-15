from scapy.all import ARP, Ether, srp


def scan_network(ip_range, timeout=5):
    """
    Scans the network for devices.

    Args:
        ip_range (str): The IP range to scan, e.g., '192.168.1.0/24'.
        timeout (int): Timeout for ARP requests in seconds.

    Returns:
        list: List of devices with IP and MAC addresses.
    """
    # Create an ARP request packet
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Send the packet and receive the responses
    answered_list = srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]

    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


if __name__ == "__main__":
    import os

    # Define the IP range (change this to match your network)
    ip_range = "192.168.1.0/24"
    print(f"Scanning network: {ip_range}")

    # Scan the network
    devices = scan_network(ip_range, timeout=5)

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
