import sys
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


def capitalize(word, selector):
    # ex: capitalize("abc", (True, False, True)) -> "AbC"
    chars = [char.upper() if selected else char
             for char, selected in zip(word, selector)]
    return ''.join(chars)


def case_permutations(word):
    for permutation in product([False, True], repeat=len(word)):
        yield capitalize(word, permutation)


def capitalizations(password):
    pw_without_digits = [char for char in password if not char.isdigit()]
    for permutation in case_permutations(pw_without_digits):
        perm_letter = iter(permutation)
        yield ''.join(
            char if char.isdigit() else next(perm_letter) for char in password)


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('IP_address')
arg_parser.add_argument('port', type=int)
cli_args = arg_parser.parse_args()

with socket.socket() as client:
    client.connect((cli_args.IP_address, cli_args.port))
    for password in generate_all_passwords():
        client.send(password.encode())
        response = client.recv(32).decode()
        if response == 'Connection success!':
            print(password)
            break
