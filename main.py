#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address to assign to interface")

    (options, arguments) = parser.parse_args()
    if not options.new_mac:
        parser.error("[.] Please specify a new mac, use --help for more info")
    elif not options.interface:
        parser.error("[.] Please specify an interface, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call("ifconfig " + interface + " down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    subprocess.call("ifconfig " + interface + " up", shell=True)


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read the MAC Address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[+] Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)
changed_mac = get_current_mac(options.interface)
if changed_mac == options.new_mac:
    print("[+] MAC Change Successful")
    print("[+] New MAC of " + options.interface + " is: " + str(changed_mac))
else:
    print("[-] MAC address did not get changed")
