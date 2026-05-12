from __future__ import annotations

import json
from pathlib import Path

from docugen.generators import generate_html as render_html
from docugen.generators import generate_pdf as render_pdf
from docugen.ir_generator import build_ir
from docugen.parser import parse_source
from docugen.semantic_analyzer import analyze_semantics
from docugen.symbol_table import SymbolTable
from docugen.visualization import build_mermaid_ast



def analyze_project(
    project_path,
    output_dir,
    generate_html=True,
    generate_pdf=True,
    generate_ast=True,
    generate_ir=True,
):
    """Run DocuGen compiler pipeline: Lex -> Parse -> AST -> IR -> HTML/PDF."""
    project_root = Path(project_path)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    if project_root.is_file() and project_root.suffix == ".py":
        source_files = [project_root]
    elif project_root.is_dir():
        source_files = sorted(project_root.rglob("*.py"))
    else:
        raise FileNotFoundError(f"No python source found at: {project_path}")

    modules = []
    parser_errors: list[str] = []
    semantic_warnings: list[str] = []
    symbol_table = SymbolTable()

    for source_file in source_files:
        module_name = source_file.stem
        source_label = source_file.name
        source_code = source_file.read_text(encoding="utf-8")
        module, errors = parse_source(source_code, module_name=module_name)
        modules.append(module)
        parser_errors.extend([f"{source_label}: {error}" for error in errors])
        semantic_warnings.extend(
            [f"{source_label}: {warning}" for warning in analyze_semantics(module)]
        )
        symbol_table.build_from_module(module)

    ir = build_ir(modules, semantic_warnings + parser_errors, symbol_table.to_dict())

    mermaid_graph = build_mermaid_ast(modules) if generate_ast else ""
    outputs: dict[str, str] = {}

    if generate_ast:
        ast_path = output_root / "ast.mmd"
        ast_path.write_text(mermaid_graph, encoding="utf-8")
        outputs["ast"] = str(ast_path)

    if generate_ir:
        ir_path = output_root / "ir.json"
        ir_path.write_text(json.dumps(ir, indent=2), encoding="utf-8")
        outputs["ir"] = str(ir_path)

    if generate_html:
        html_path = output_root / "output.html"
        render_html(ir, mermaid_graph, html_path)
        outputs["html"] = str(html_path)

    if generate_pdf:
        pdf_path = output_root / "output.pdf"
        render_pdf(ir, pdf_path)
        outputs["pdf"] = str(pdf_path)

    return {
        "modules": [module.to_dict() for module in modules],
        "warnings": semantic_warnings,
        "errors": parser_errors,
        "outputs": outputs,
    }


__all__ = ["analyze_project"]
