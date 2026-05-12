"""Lexical analyzer for DocuGen using PLY."""

from __future__ import annotations

import keyword
from typing import List, Tuple

import ply.lex as lex

KEYWORDS = set(keyword.kwlist)


tokens = [
    "KEYWORD",
    "IDENTIFIER",
    "INTEGER_LITERAL",
    "FLOAT_LITERAL",
    "STRING_LITERAL",
    "DOCSTRING",
    "COMMENT",
    "OPERATOR",
    "DELIMITER",
]


def _with_column(token):
    token.column = token.lexpos - token.lexer.line_start + 1
    return token


def t_DOCSTRING(t):
    r'("""(.|\n)*?"""|\'\'\'(.|\n)*?\'\'\')'
    newline_count = t.value.count("\n")
    if newline_count:
        t.lexer.lineno += newline_count
        t.lexer.line_start = t.lexpos + t.value.rfind("\n") + 1
    return _with_column(t)


def t_COMMENT(t):
    r'\#.*'
    return _with_column(t)


def t_FLOAT_LITERAL(t):
    r'(\d+\.\d*|\.\d+)([eE][+-]?\d+)?|\d+[eE][+-]?\d+'
    return _with_column(t)


def t_INTEGER_LITERAL(t):
    r'\d+'
    return _with_column(t)


def t_STRING_LITERAL(t):
    r'(\'([^\\\n\']|\\.)*\'|"([^\\\n"]|\\.)*")'
    return _with_column(t)


def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in KEYWORDS:
        t.type = "KEYWORD"
    return _with_column(t)


def t_OPERATOR(t):
    r'\*\*=|//=|<<=|>>=|==|!=|<=|>=|\+=|-=|\*=|/=|%=|\*\*|//|<<|>>|:=|->|[+\-*/%&|^~<>.=]'
    return _with_column(t)


def t_DELIMITER(t):
    r'[()\[\]{},:;@]'
    return _with_column(t)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.line_start = t.lexpos + len(t.value)


t_ignore = " \t\r\f\v"


def t_error(t):
    column = t.lexpos - t.lexer.line_start + 1
    t.lexer.errors.append(
        f"Invalid character {t.value[0]!r} at line {t.lineno}, column {column}"
    )
    t.lexer.skip(1)


def build_lexer(**kwargs):
    lexer = lex.lex(**kwargs)
    lexer.line_start = 0
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
