#!/Users/tharundv/Projects/HoneyPot/.env/bin/python

import logging
from logging.handlers import RotatingFileHandler
import socket


logging_format = logging.Formatter('%(message)s')

funnel_logging = logging.getLogger("FunnelLogger")
funnel_logging.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler("audits.log",maxBytes=2000,backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logging.addHandler(funnel_handler)

creds_logging = logging.getLogger("CredsLogger")
creds_logging.setLevel(logging.INFO)
creds_handler = RotatingFileHandler("cmd_audit.log",maxBytes=2000,backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logging.addHandler(creds_handler)


# Emulated Shells

def emulated_shell(channel,clinet_ip):
    channel.send(b'corporate-jumpbox2$ ')
    command = b""
    while True:
        char = channel.recv(1)
        channel.send(char)
        if not char:
            channel.close()
        command += char

        if char == b'\r':
            if command.strip() == b'exit':
                response = b'\nBye\n'
                channel.close()
            elif command.strip() == b'pwd':
                response = b'\n/home/corporate-jumpbox2' + b'\r\n'
            elif command.strip() == b'whoami':
                response = b'\ncorportate-jumpbox2' + b'\r\n'

        channel.send(response)
        channel.send(b'corporate-jumpbox2$ ')
        command = b""
