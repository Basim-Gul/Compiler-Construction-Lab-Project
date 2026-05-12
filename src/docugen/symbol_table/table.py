"""Simple symbol table stubs for scope management."""

from __future__ import annotations

from dataclasses import dataclass, field

from docugen.ast_engine import ModuleNode


@dataclass
class Scope:
    name: str
    symbols: dict[str, str] = field(default_factory=dict)


class SymbolTable:
    def __init__(self) -> None:
        self.global_scope = Scope(name="global")
        self.function_scopes: dict[str, Scope] = {}

    def build_from_module(self, module: ModuleNode) -> None:
        for function in module.functions:
            self.global_scope.symbols[function.name] = "function"
            scope = Scope(name=function.name)
            for parameter in function.parameters:
                scope.symbols[parameter.name] = parameter.annotation or "unknown"
            self.function_scopes[function.name] = scope
        for klass in module.classes:
            self.global_scope.symbols[klass.name] = "class"
            for method in klass.methods:
                scoped_name = f"{klass.name}.{method.name}"
                self.global_scope.symbols[scoped_name] = "method"
                scope = Scope(name=scoped_name)
                for parameter in method.parameters:
                    scope.symbols[parameter.name] = parameter.annotation or "unknown"
                self.function_scopes[scoped_name] = scope

    def to_dict(self) -> dict[str, dict[str, dict[str, str]]]:
        return {
            "global": {"symbols": self.global_scope.symbols},
            "functions": {
                name: {"symbols": scope.symbols}
                for name, scope in self.function_scopes.items()
            },
        }
