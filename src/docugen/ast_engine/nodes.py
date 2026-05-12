from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocstringNode:
    value: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Docstring", "value": self.value}


@dataclass
class ParameterNode:
    name: str
    annotation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "annotation": self.annotation,
        }


@dataclass
class FunctionNode:
    name: str
    parameters: list[ParameterNode] = field(default_factory=list)
    returns: str | None = None
    docstring: DocstringNode | None = None
    decorators: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "Function",
            "name": self.name,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
            "returns": self.returns,
            "docstring": self.docstring.to_dict() if self.docstring else None,
            "decorators": self.decorators,
        }


@dataclass
class ClassNode:
    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionNode] = field(default_factory=list)
    docstring: DocstringNode | None = None
    decorators: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "Class",
            "name": self.name,
            "bases": self.bases,
            "methods": [method.to_dict() for method in self.methods],
            "docstring": self.docstring.to_dict() if self.docstring else None,
            "decorators": self.decorators,
        }


@dataclass
class ModuleNode:
    name: str
    functions: list[FunctionNode] = field(default_factory=list)
    classes: list[ClassNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "Module",
            "name": self.name,
            "functions": [function.to_dict() for function in self.functions],
            "classes": [klass.to_dict() for klass in self.classes],
        }
