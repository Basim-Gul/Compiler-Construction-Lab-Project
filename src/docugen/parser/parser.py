"""PLY parser for extracting basic Python function signatures and docstrings."""

from __future__ import annotations

from dataclasses import dataclass, field

import ply.yacc as yacc

from docugen.ast_engine import DocstringNode, FunctionNode, ModuleNode, ParameterNode
from docugen.lexer.lexer import build_lexer, tokens


@dataclass
class ParserState:
    module_name: str
    errors: list[str] = field(default_factory=list)


_parser_state: ParserState | None = None


def p_module(p):
    "module : elements"
    p[0] = ModuleNode(name=_parser_state.module_name, functions=p[1])


def p_elements_recursive(p):
    "elements : elements element"
    if p[2] is None:
        p[0] = p[1]
    elif isinstance(p[2], FunctionNode):
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]


def p_elements_empty(p):
    "elements : empty"
    p[0] = []


def p_element_function(p):
    "element : function_def"
    p[0] = p[1]


def p_element_junk(p):
    "element : junk"
    p[0] = None


def p_function_def(p):
    "function_def : DEF IDENTIFIER LPAREN parameter_list RPAREN return_annotation_opt COLON function_body"
    p[0] = FunctionNode(
        name=p[2],
        parameters=p[4],
        returns=p[6],
        docstring=p[8],
    )


def p_parameter_list_empty(p):
    "parameter_list : empty"
    p[0] = []


def p_parameter_list_items(p):
    "parameter_list : parameter_items"
    p[0] = p[1]


def p_parameter_items_single(p):
    "parameter_items : parameter"
    p[0] = [p[1]]


def p_parameter_items_multi(p):
    "parameter_items : parameter_items COMMA parameter"
    p[0] = p[1] + [p[3]]


def p_parameter(p):
    "parameter : IDENTIFIER annotation_opt"
    p[0] = ParameterNode(name=p[1], annotation=p[2])


def p_annotation_opt(p):
    """annotation_opt : COLON IDENTIFIER
    | empty"""
    p[0] = p[2] if len(p) == 3 else None


def p_return_annotation_opt(p):
    """return_annotation_opt : ARROW IDENTIFIER
    | empty"""
    p[0] = p[2] if len(p) == 3 else None


def p_function_body(p):
    "function_body : skip_newlines docstring_opt"
    p[0] = p[2]


def p_skip_newlines_more(p):
    "skip_newlines : skip_newlines NEWLINE"


def p_skip_newlines_empty(p):
    "skip_newlines : empty"


def p_docstring_opt(p):
    """docstring_opt : DOCSTRING
    | STRING
    | empty"""
    if len(p) == 2 and isinstance(p[1], str):
        cleaned = p[1].strip('"\'')
        p[0] = DocstringNode(value=cleaned)
    else:
        p[0] = None


def p_junk(p):
    """junk : IDENTIFIER
    | LPAREN
    | RPAREN
    | COLON
    | COMMA
    | ARROW
    | DOCSTRING
    | STRING
    | NEWLINE
    | OTHER
    | DEF"""


def p_empty(p):
    "empty :"


def p_error(p):
    if p is not None and _parser_state is not None:
        _parser_state.errors.append(f"Syntax issue near token {p.type} ({p.value!r})")


_parser = yacc.yacc(start="module", write_tables=False, debug=False)


def parse_source(source_code: str, module_name: str = "module") -> tuple[ModuleNode, list[str]]:
    global _parser_state
    _parser_state = ParserState(module_name=module_name)
    lexer = build_lexer()
    module = _parser.parse(source_code, lexer=lexer)
    errors = list(lexer.errors) + _parser_state.errors
    return module or ModuleNode(name=module_name), errors
