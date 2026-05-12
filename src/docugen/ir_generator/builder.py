"""IR builder for DocuGen AST output."""

from __future__ import annotations

from docugen.ast_engine import ModuleNode


def build_ir(
    modules: list[ModuleNode],
    semantic_warnings: list[str],
    parser_errors: list[str],
    symbol_table: dict,
) -> dict:
    return {
        "modules": [module.to_dict() for module in modules],
        "semantic_warnings": semantic_warnings,
        "parser_errors": parser_errors,
        "symbol_table": symbol_table,
    }
