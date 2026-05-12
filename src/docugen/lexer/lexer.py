"""PLY lexer for simple Python function/docstring extraction."""

from __future__ import annotations

import ply.lex as lex


tokens = (
    "CLASS",
    "DEF",
    "IDENTIFIER",
    "NUMBER",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "LPAREN",
    "RPAREN",
    "DOT",
    "COLON",
    "COMMA",
    "ASSIGN",
    "PLUS",
    "MINUS",
    "STAR",
    "SLASH",
    "AT",
    "ARROW",
    "DOCSTRING",
    "STRING",
    "NEWLINE",
    "OTHER",
)


def t_CLASS(t):
    r"class\b"
    return t


def t_ARROW(t):
    r"->"
    return t


def t_DOT(t):
    r"\."
    return t


def t_ASSIGN(t):
    r"="
    return t


def t_PLUS(t):
    r"\+"
    return t


def t_MINUS(t):
    r"-"
    return t


def t_STAR(t):
    r"\*"
    return t


def t_SLASH(t):
    r"/"
    return t


def t_AT(t):
    r"@"
    return t


def t_LBRACKET(t):
    r"\["
    return t


def t_RBRACKET(t):
    r"\]"
    return t


def t_LBRACE(t):
    r"\{"
    return t


def t_RBRACE(t):
    r"\}"
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


def t_NUMBER(t):
    r"((\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?|\d+)"
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


t_OTHER = r"[%&|^~<>!?;#]+"


t_ignore = " \t\r\f\v"


def t_error(t):
    line_start = t.lexer.lexdata.rfind("\n", 0, t.lexpos) + 1
    column = t.lexpos - line_start + 1
    t.lexer.errors.append(
        f"Invalid character {t.value[0]!r} at line {t.lineno}, column {column}"
    )
    t.lexer.skip(1)


def build_lexer(**kwargs):
    lexer = lex.lex(**kwargs)
    lexer.errors = []
    return lexer


def tokenize(source_code: str) -> tuple[list[lex.LexToken], list[str]]:
    lexer = build_lexer()
    lexer.input(source_code)
    token_stream: list[lex.LexToken] = []
    while True:
        token = lexer.token()
        if not token:
            break
        token_stream.append(token)
    return token_stream, lexer.errors
