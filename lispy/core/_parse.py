"""parse tokens into expressions"""

import re

PAREN = re.compile(r"[()]")
INT = re.compile(r"\d+")
FLOAT = re.compile(r"\d+[.]\d*")


def parse(tokens):
    """parse tokens into a list of expressions"""

    def _parse(tokens, paren):
        parsed = []
        while tokens:
            token = tokens[0]
            tokens = tokens[1:]
            if token == ")":
                if paren:
                    return parsed, tokens
                raise ParseError("mismatched parenthesis")
            elif token == "(":
                sub, tokens = _parse(tokens, True)
                parsed.append(sub)
            elif FLOAT.match(token):
                parsed.append(float(token))
            elif INT.match(token):
                parsed.append(int(token))
            else:
                parsed.append(token)
        if paren:
            raise ParseError("mismatched parenthesis")
        if len(parsed) == 1:
            parsed = parsed[0]
        return parsed, tokens

    parsed, _ = _parse(tokens, False)
    return parsed


class ParseError(Exception):
    pass
