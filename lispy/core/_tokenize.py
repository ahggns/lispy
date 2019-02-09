"""tokenize strings"""

import re

WHITESPACE = re.compile(r"\s")
PAREN = re.compile(r"[()]")
NUMERIC = re.compile(r"\d+([.]\d*)?")
STRING = re.compile(r'"[^"]*"')
IDENTIFIER = re.compile(r"[A-Za-z_*/\-+]+[A-Za-z0-9_]*")


def _match(string):
    for definition in (PAREN, NUMERIC, STRING, IDENTIFIER):
        match = definition.match(string)
        if match:
            token = match.group(0)
            return token
    raise ValueError("could not tokenize '{}'".format(string))


def tokenize(string):
    """split string into tokens"""
    tokens = []
    while string:
        if WHITESPACE.match(string):
            string = string[1:]
        else:
            token = _match(string)
            tokens.append(token)
            string = string[len(token) :]
    return tokens
