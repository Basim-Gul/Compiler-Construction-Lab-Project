"""AST visualization utilities."""

from __future__ import annotations

from graphviz import Digraph

from docugen.ast_engine import ModuleNode


def _mermaid_label(text: str, limit: int = 60) -> str:
    normalized = " ".join(text.split())
    return normalized[:limit].replace('"', "'")


def _dot_label(text: str, limit: int = 60) -> str:
    normalized = " ".join(text.split())[:limit]
    return normalized.replace("\\", "\\\\").replace('"', '\\"')


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
                doc_preview = _mermaid_label(function.docstring.value)
                lines.append(f"{doc_id}[\"Docstring: {doc_preview}\"]")
                lines.append(f"{function_id} --> {doc_id}")
            for parameter_index, parameter in enumerate(function.parameters):
                parameter_id = f"{function_id}_P{parameter_index}"
                annotation = parameter.annotation or "untyped"
                lines.append(
                    f"{parameter_id}[\"Param: {parameter.name} ({annotation})\"]"
                )
                lines.append(f"{function_id} --> {parameter_id}")
        for class_index, klass in enumerate(module.classes):
            class_id = f"{module_id}_C{class_index}"
            lines.append(f"{class_id}[\"Class: {klass.name}\"]")
            lines.append(f"{module_id} --> {class_id}")
            for method_index, method in enumerate(klass.methods):
                method_id = f"{class_id}_M{method_index}"
                lines.append(f"{method_id}[\"Method: {method.name}\"]")
                lines.append(f"{class_id} --> {method_id}")
                for parameter_index, parameter in enumerate(method.parameters):
                    parameter_id = f"{method_id}_P{parameter_index}"
                    annotation = parameter.annotation or "untyped"
                    lines.append(
                        f"{parameter_id}[\"Param: {parameter.name} ({annotation})\"]"
                    )
                    lines.append(f"{method_id} --> {parameter_id}")
    return "\n".join(lines)


def build_graphviz_ast(modules: list[ModuleNode]) -> str:
    graph = Digraph("DocuGenAST")
    graph.attr(rankdir="TB")
    for module_index, module in enumerate(modules):
        module_id = f"M{module_index}"
        graph.node(module_id, f"Module: {module.name}", shape="box")
        for function_index, function in enumerate(module.functions):
            function_id = f"{module_id}_F{function_index}"
            graph.node(function_id, f"Function: {function.name}", shape="ellipse")
            graph.edge(module_id, function_id)
            if function.docstring:
                doc_id = f"{function_id}_D"
                graph.node(
                    doc_id,
                    f"Doc: {_dot_label(function.docstring.value)}",
                    shape="note",
                )
                graph.edge(function_id, doc_id)
            for parameter_index, parameter in enumerate(function.parameters):
                parameter_id = f"{function_id}_P{parameter_index}"
                annotation = parameter.annotation or "untyped"
                graph.node(parameter_id, f"{parameter.name}: {annotation}")
                graph.edge(function_id, parameter_id)
        for class_index, klass in enumerate(module.classes):
            class_id = f"{module_id}_C{class_index}"
            graph.node(class_id, f"Class: {klass.name}", shape="box3d")
            graph.edge(module_id, class_id)
            for method_index, method in enumerate(klass.methods):
                method_id = f"{class_id}_M{method_index}"
                graph.node(method_id, f"Method: {method.name}", shape="ellipse")
                graph.edge(class_id, method_id)
                for parameter_index, parameter in enumerate(method.parameters):
                    parameter_id = f"{method_id}_P{parameter_index}"
                    annotation = parameter.annotation or "untyped"
                    graph.node(parameter_id, f"{parameter.name}: {annotation}")
                    graph.edge(method_id, parameter_id)
    return graph.source
