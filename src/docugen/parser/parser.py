"""Parser for extracting Python modules, classes, methods and functions."""

from __future__ import annotations

import ast

from docugen.ast_engine import ClassNode, DocstringNode, FunctionNode, ModuleNode, ParameterNode


def _stringify(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def _build_parameters(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ParameterNode]:
    args: list[ast.arg] = [
        *function.args.posonlyargs,
        *function.args.args,
        *function.args.kwonlyargs,
    ]
    if function.args.vararg is not None:
        args.append(function.args.vararg)
    if function.args.kwarg is not None:
        args.append(function.args.kwarg)
    return [
        ParameterNode(name=argument.arg, annotation=_stringify(argument.annotation))
        for argument in args
    ]


def _build_docstring(node: ast.AST) -> DocstringNode | None:
    text = ast.get_docstring(node, clean=False)
    return DocstringNode(value=text) if text else None


def _build_function(function: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionNode:
    return FunctionNode(
        name=function.name,
        parameters=_build_parameters(function),
        returns=_stringify(function.returns),
        docstring=_build_docstring(function),
        decorators=[_stringify(decorator) or "" for decorator in function.decorator_list if _stringify(decorator)],
    )


def _build_class(klass: ast.ClassDef) -> ClassNode:
    methods = [
        _build_function(node)
        for node in klass.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return ClassNode(
        name=klass.name,
        bases=[_stringify(base) or "" for base in klass.bases if _stringify(base)],
        methods=methods,
        docstring=_build_docstring(klass),
        decorators=[_stringify(decorator) or "" for decorator in klass.decorator_list if _stringify(decorator)],
    )


def parse_source(source_code: str, module_name: str = "module") -> tuple[ModuleNode, list[str]]:
    try:
        root = ast.parse(source_code)
    except SyntaxError as exc:
        message = f"Syntax issue at line {exc.lineno}, column {exc.offset}: {exc.msg}"
        return ModuleNode(name=module_name), [message]

    functions: list[FunctionNode] = []
    classes: list[ClassNode] = []
    for node in root.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(_build_function(node))
        elif isinstance(node, ast.ClassDef):
            classes.append(_build_class(node))

    return ModuleNode(name=module_name, functions=functions, classes=classes), []
