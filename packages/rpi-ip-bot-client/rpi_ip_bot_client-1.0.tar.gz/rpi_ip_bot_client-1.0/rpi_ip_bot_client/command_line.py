import sys
import os
from argparse import ArgumentParser
from string import Template


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("operation", type=str,
        help="install or uninstall")
    arg_parser.add_argument("token", type=str, nargs='?',
        help="A token generated with the /add command")
    arg_parser.add_argument("--dir", default="/etc/network/if-up.d",
        help="A directory the script should be placed to")
    args = arg_parser.parse_args(sys.argv[1:])
    if args.operation == "install":
        if args.token:
            try:
                with open(args.dir+"/rpi_ip_bot_client", "w") as script:
                    print(args.token)
                    script.write(Template(DATA).safe_substitute({"TOKEN": args.token}))
            except IOError:
                print("ERROR: cannot write to the specified directory! Maybe the root permissions are required or the directory doesn't exist.")
                exit(0)
        else:
            print("ERROR: a token is required to install the script.")
            exit(0)
    elif args.operation == "uninstall":
        try:
            os.remove(args.dir+"/rpi_ip_bot_client")
        except OSError:
            print("ERROR: cannot write to the specified directory! Maybe the root permissions are required or the directory doesn't exist.")
            exit(0)
    else:
        print("ERROR: the wrong operation name! Excecting install or uninstall")

DATA="""
#!/usr/bin/env python3

import requests
import json
import socket

TOKEN = "${TOKEN}"
url = "https://rpi-ip-bot.herokuapp.com/recieve_ip"
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    internal_ip = s.getsockname()[0]
    payload = {
        "token": TOKEN,
        "external_ip": requests.get('https://ipapi.co/ip/').text,
        "internal_ip": internal_ip
    }
    requests.post(url, data=json.dumps(payload))
    connected=True
except OSError:
    pass
except requests.exceptions.ConnectionError:
    pass
"""
