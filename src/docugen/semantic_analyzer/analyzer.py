"""Semantic analyzer stubs for DocuGen."""

from __future__ import annotations

from docugen.ast_engine import ModuleNode


def analyze_semantics(module: ModuleNode) -> list[str]:
    warnings: list[str] = []
    for function in module.functions:
        if function.docstring is None:
            warnings.append(f"Function '{function.name}' is missing a docstring.")
        for parameter in function.parameters:
            if parameter.annotation is None:
                warnings.append(
                    f"Parameter '{parameter.name}' in function '{function.name}' is missing a type annotation."
                )
    return warnings
