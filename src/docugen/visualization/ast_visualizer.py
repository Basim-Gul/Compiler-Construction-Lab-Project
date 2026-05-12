"""AST visualization utilities."""

from __future__ import annotations

from docugen.ast_engine import ModuleNode


def build_mermaid_ast(modules: list[ModuleNode]) -> str:
    lines = ["graph TD"]
    for module_index, module in enumerate(modules):
        module_id = f"M{module_index}"
        lines.append(f"{module_id}[\"Module: {module.name}\"]")
        for function_index, function in enumerate(module.functions):
            function_id = f"{module_id}_F{function_index}"
            lines.append(f"{function_id}[\"Function: {function.name}\"]")
            lines.append(f"{module_id} --> {function_id}")
            if function.docstring:
                doc_id = f"{function_id}_D"
                doc_preview = function.docstring.value.replace('"', "'")[:60]
                lines.append(f"{doc_id}[\"Docstring: {doc_preview}\"]")
                lines.append(f"{function_id} --> {doc_id}")
            for parameter_index, parameter in enumerate(function.parameters):
                parameter_id = f"{function_id}_P{parameter_index}"
                annotation = parameter.annotation or "untyped"
                lines.append(
                    f"{parameter_id}[\"Param: {parameter.name} ({annotation})\"]"
                )
                lines.append(f"{function_id} --> {parameter_id}")
    return "\n".join(lines)
