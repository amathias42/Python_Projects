import sys
import subprocess

# TODO: docstrings


def eth_to_dhcp(interface_name="Ethernet"):
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
    bitmask = None
    if "\\" in ip or "/" in ip:
        slashIndex = max(ip.find("\\"), ip.find("/"))
        bitmask = ip[slashIndex + 1 :]
        ip = ip[:slashIndex]
    return ip, bitmask


def checkIP(ip):
    pureIP, bitmask = isolate_bitmask(ip)

    if bitmask is not None:
        try:
            int(bitmask)
        except ValueError:
            print("Bitmask (ip.ip.ip.ip/bitmask) must be an integer")
            return False

    if not checkNetAddress(pureIP.split("."), typeStr="IP"):
        return False

    return True


def checkNetmask(netmask):
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
    byteGroups = gateway.split(".")

    if not checkNetAddress(byteGroups, "gateway"):
        return False

    if not inSubnet(ip, gateway, netmask):
        print("Gateway not in subnet of static IP address")
        return False

    return True


def checkNetAddress(byteGroups, typeStr=""):
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
            print(typeStr + " address bytes must be in the range [0,255]")
            return False

    return True


def inSubnet(ip1, ip2, netmask):
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
    ip = input("ip: ")
    while not checkIP:
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
