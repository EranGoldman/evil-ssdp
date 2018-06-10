#!/usr/bin/env python3

from lib.classes import SSDPListener
from lib.classes import DeviceDescriptor
import os,sys,re,argparse;

banner = r'''
___________     .__.__    _________ _________________ __________
\_   _____/__  _|__|  |  /   _____//   _____/\______ \\______   \
 |    __)_\  \/ /  |  |  \_____  \ \_____  \  |    |  \|     ___/
 |        \\   /|  |  |__/        \/        \ |    `   \    |
/_______  / \_/ |__|____/_______  /_______  //_______  /____|
        \/                      \/        \/         \/

...by initstring
'''

print(banner)

# Handle arguments before moving on....
parser = argparse.ArgumentParser()
parser.add_argument('interface', type=str, help='Network interface to listen on.', action='store')
args = parser.parse_args()
interface = args.interface

# Set up some nice colors
class bcolors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    ORANGE = '\033[93m'
    ENDC = '\033[0m'
okBox = bcolors.BLUE + '[*] ' + bcolors.ENDC
NoteBox = bcolors.GREEN + '[+] ' + bcolors.ENDC
warnBox = bcolors.ORANGE + '[!] ' + bcolors.ENDC


def get_ip(i):
    try:
        ip = re.findall(r'inet (.*?)/', os.popen('ip addr show ' + i).read())[0]
        broadcast = re.findall(r'brd (.*?) ', os.popen('ip addr show ' + i).read())[0]
        return ip,broadcast
    except Exception:
        print(warnBox + "Could not get network interface info. Please check and try again.")
        sys.exit()

def listen_msearch(ip):
   print(okBox + "Listening for MSEARCH queries using {}.".format(interface))
   listener = SSDPListener()
   listener.run(ip)


def serve_descriptor(i):
    print(okBox + "Serving device descriptor using {} at {}".format(interface,i))
    descriptor = DeviceDescriptor(i)


def main():
   ip,broadcast = get_ip(interface)
   listen_msearch(ip)
   serve_descriptor(ip)

if __name__ == "__main__":
    main()
