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

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "Function",
            "name": self.name,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
            "returns": self.returns,
            "docstring": self.docstring.to_dict() if self.docstring else None,
        }


@dataclass
class ModuleNode:
    name: str
    functions: list[FunctionNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "Module",
            "name": self.name,
            "functions": [function.to_dict() for function in self.functions],
        }
