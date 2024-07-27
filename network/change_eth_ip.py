"""Modify the IPv4 settings of a network interface on Windows.

The IPv4 address and settings can be set to DHCP or static addressing. If set to static addressing,
the script will prompt for address, netmask, and gateway. It will verify the inputs and ask for
another entry if the original input was determined to be invalid.
It checks:
- addresses are in the IPv4 quad-dotted notation or IPv4-CIDR format
- the netmask is contiguous
- the subnet mask is an integer if specified in CIDR 
- the gateway & address are in the same subnet created by the netmask

Usage:

    python change_eth_ip.py ["s" or "d"]"""

import sys
import subprocess


def eth_to_dhcp(interface_name="Ethernet"):
    """Changes network interface to DHCP via netsh command.

    Args:
        interface_name: The name of the network interface. str."""
    subprocess.run(
        [
            "netsh",
            "interface",
            "ip",
            "set",
            "address",
            "name=",
            '"' + str(interface_name) + '"',
            "dhcp",
        ],
        check=False,
    )


def eth_to_static(ip, netmask, gateway=None, interface_name="Ethernet"):
    """Changes network interface to static IPv4 via netsh command.

    Args:
        ip: IPv4 address. quad-dotted notation in str
        netmask: subnet mask. quad-dotted notation in str
        gateway: gateway address. quad-dotted notation in str. optional"""
    staticIPList = [
        "netsh",
        "interface",
        "ip",
        "set",
        "address",
        "name=",
        '"' + str(interface_name) + '"',
        "static",
        str(ip),
        str(netmask),
    ]

    if gateway is not None:
        staticIPList.append(str(gateway))

    subprocess.run(
        staticIPList,
        check=False,
    )


def isolate_bitmask(ip):
    """Isolates subnet bistmask from IP address if expressed in CIDR.

    Args:
        ip: IP address. quad-dotted notation in str

    Returns:
        A tuple of (ip, bitmask)

        ip: input arg ip truncated after (inclusively) "/" or "\\"
        bitmask: characters after "/" or "\\" if present, otherwise None"""
    bitmask = None
    if "\\" in ip or "/" in ip:
        slashIndex = max(ip.find("\\"), ip.find("/"))
        bitmask = ip[slashIndex + 1 :]
        ip = ip[:slashIndex]
    return ip, bitmask


def checkIP(ip):
    """Checks if IPv4 address is valid.

    Separates CIDR bitmask if present, checks if bitmask is an integer [0,32],
    and checks address is in proper quad-dotted format.

    Args:
        ip: IPv4 address to be checked. str

    Returns:
        True if @arg ip is strictly "[0-255].[0-255].[0-255].[0-255](["/" or "\\"][0-32])",
        otherwise False"""
    pureIP, bitmask = isolate_bitmask(ip)

    if bitmask is not None:
        try:
            int(bitmask)
            if bitmask not in range(33):
                print("Bitmask must be an integer [0-32]")
                return False
        except ValueError:
            print("Bitmask (ip.ip.ip.ip/bitmask) must be an integer [0-32]")
            return False

    if not checkNetAddress(pureIP.split("."), typeStr="IP"):
        return False

    return True


def checkNetmask(netmask):
    """Checks if subnet mask is quad-dotted and binary-contiguous.

    Args:
        netmask: subnet mask to be checked. str

    Returns:
        True if @arg netmask is strictly "[0-255].[0-255].[0-255].[0-255]",
        and a contiguous mask of 1s when represented in binary,
        otherwise False"""
    VALID_NETMASK_BYTES = [255, 254, 252, 248, 240, 224, 192, 128, 0]
    byteGroups = netmask.split(".")

    if not checkNetAddress(byteGroups, typeStr="netmask"):
        return False

    lastB = 256

    for b in byteGroups:
        bInt = int(b)

        if bInt > lastB or bInt not in VALID_NETMASK_BYTES:
            print("Netmask must be contiguous")
            return False

    return True


def checkGateway(gateway, ip, netmask):
    """Checks if gateway is a valid net address and in the same subnet as ip&netmask

    Args:
        gateway: gateway to be checked. str
        ip: ip address to compare with gateway for subnet check. quad-dotted notation in str
        netmask: netmask to compare with ip & gateway for subnet check. quad-dotted notation in str

    Returns:
        True if @arg gateway is strictly "[0-255].[0-255].[0-255].[0-255]",
        and if @arg gateway is in the subnet created by @arg ip & @arg netmask,
        otherwise False"""
    byteGroups = gateway.split(".")

    if not checkNetAddress(byteGroups, "gateway"):
        return False

    if not inSubnet(ip, gateway, netmask):
        print("Gateway not in subnet of static IP address")
        return False

    return True


def checkNetAddress(byteGroups, typeStr=""):
    """Checks is a net address is in quad-dotted format.

    Args:
        byteGroups: list of strings representing the 4 bytes in a quad-dotted address
        typeStr: type of net address to insert in invalid message. str

    Returns:
        True if @arg byteGroups contains 4 strings and each of those strings
        can be converted to an int [0-255],
        otherwise False"""
    if len(byteGroups) != 4:
        print(
            "Incorrect "
            + typeStr
            + " address format. Required format: [0-255].[0-255].[0-255].[0-255]"
        )
        return False

    for b in byteGroups:
        try:
            bInt = int(b)
        except ValueError:
            print(typeStr + " address bytes must be integers")
            return False

        if bInt < 0 or bInt > 255:
            print(typeStr + " address bytes must be in the range [0-255]")
            return False

    return True


def inSubnet(ip1, ip2, netmask):
    """Check if two ip address are in the same subnet specified by the subnet mask

    Args:
        ip1: first ip address for compare. quad-dotted notation in str
        ip2: second ip address for compare. quad-dotted notation in str
        netmask: subnet mask to mask ip1 & ip2. quad-dotted notation in str

    Returns:
        True if each byte in ip1 when bitwise-AND-ed with the corresponding byte
        in the subnet mask is equivalent to the corresponding bitwise-AND-ed byte
        of ip2 with the subnet mask,
        otherwise False"""

    ip1Bytes = ip1.split(".")
    ip2Bytes = ip2.split(".")
    netmaskBytes = netmask.split(".")

    for i, b in enumerate(netmaskBytes):
        b1Mask = int(b) & int(ip1Bytes[i])
        b2Mask = int(b) & int(ip2Bytes[i])
        if b1Mask != b2Mask:
            return False

    return True


def bitmask_to_netmask(bitmask):
    """Converts a CIDR notation bitmask to a quad-dotted notation subnet mask.

    Args:
        bitmask: CIDR notation bitmask. int [0-32]

    Returns:
        A string representing the CIDR bitmask in quad-dotted notation"""
    bitmask = int(bitmask)
    bitmaskBinary = ""

    for _ in range(32):
        if bitmask > 0:
            bitmaskBinary = bitmaskBinary + "1"
            bitmask = bitmask - 1
        else:
            bitmaskBinary = bitmaskBinary + "0"

    h1 = bitmaskBinary[: len(bitmaskBinary) // 2]
    h2 = bitmaskBinary[len(bitmaskBinary) // 2 :]

    q1 = h1[: len(h1) // 2]
    q2 = h1[len(h1) // 2 :]
    q3 = h2[: len(h2) // 2]
    q4 = h2[len(h2) // 2 :]

    netmask = (
        str(int(q1, 2))
        + "."
        + str(int(q2, 2))
        + "."
        + str(int(q3, 2))
        + "."
        + str(int(q4, 2))
    )
    return netmask


def ask_settings():
    """CLI prompts for ip, netmask, and gateway.

    Asks for ip address, netmask (if not expressed with ip in CIDR notation),
    and gateway - asking again if input is invalid. Allows {Enter} or 0 to be entered
    for the selection of not setting a gateway address.

    Returns:
        A tuple of (ip, netmask, gateway)
            ip: validated IPv4 address. quad-dotted notation in str
            netmask: validated IPv4 subnet mask. quad-dotted notation in str
            gateway: either None or validated IPv4 gateway address. quad-dotted notation in str
    """
    ip = input("ip: ")
    while not checkIP(ip):
        ip = input("ip: ")
    ip, bitmask = isolate_bitmask(ip)
    if bitmask is not None:
        netmask = bitmask_to_netmask(bitmask)
    else:
        netmask = input("netmask: ")
        while not checkNetmask(netmask):
            netmask = input("netmask: ")

    gateway = input("gateway (Enter or 0 is no gateway): ")
    if gateway == "0" or gateway == "":
        gateway = None
    else:
        while (not checkGateway(gateway, ip, netmask)) and gateway is not None:
            gateway = input("gateway (Enter or 0 is no gateway): ")
            if gateway == "0" or gateway == "":
                gateway = None

    return ip, netmask, gateway


def main():
    """Changes IP setting of network interface via netsh command."""
    mode = sys.argv[1]
    if mode == "d":
        eth_to_dhcp()
    elif mode == "s":
        ip, netmask, gateway = ask_settings()
        eth_to_static(ip, netmask, gateway)
    else:
        print("Choose mode d(hcp) or s(tatic) via command line arg")
        exit(1)


if __name__ == "__main__":
    main()
