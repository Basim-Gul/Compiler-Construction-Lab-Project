"""PLY lexer for simple Python function/docstring extraction."""

from __future__ import annotations

from typing import List, Tuple

import ply.lex as lex


tokens = (
    "DEF",
    "IDENTIFIER",
    "LPAREN",
    "RPAREN",
    "COLON",
    "COMMA",
    "ARROW",
    "DOCSTRING",
    "STRING",
    "NEWLINE",
    "OTHER",
)


def t_ARROW(t):
    r"->"
    return t


def t_LPAREN(t):
    r"\("
    return t


def t_RPAREN(t):
    r"\)"
    return t


def t_COLON(t):
    r":"
    return t


def t_COMMA(t):
    r","
    return t


def t_DEF(t):
    r"def\b"
    return t


def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    return t


def t_DOCSTRING(t):
    r'("""(.|\n)*?"""|\'\'\'(.|\n)*?\'\'\')'
    t.lexer.lineno += t.value.count("\n")
    return t


def t_STRING(t):
    r'(\'([^\\\n\']|\\.)*\'|"([^\\\n"]|\\.)*")'
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


t_OTHER = r"[@\[\]{}=+\-*/%&|^~<>.!?;#]+"


t_ignore = " \t\r\f\v"


def t_error(t):
    t.lexer.errors.append(f"Invalid character {t.value[0]!r} at line {t.lineno}")
    t.lexer.skip(1)


def build_lexer(**kwargs):
    lexer = lex.lex(**kwargs)
    lexer.errors = []
    return lexer


def tokenize(source_code: str) -> Tuple[List[lex.LexToken], List[str]]:
    lexer = build_lexer()
    lexer.input(source_code)
    token_stream: List[lex.LexToken] = []
    while True:
        token = lexer.token()
        if not token:
            break
        token_stream.append(token)
    return token_stream, lexer.errors
