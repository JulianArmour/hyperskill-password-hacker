import socket
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('IP_address')
arg_parser.add_argument('port', type=int)
arg_parser.add_argument('message')
cli_args = arg_parser.parse_args()

with socket.socket() as client:
    client.connect((cli_args.IP_address, cli_args.port))
    client.send(cli_args.message.encode())
    response = client.recv(32).decode()
    print(response)
