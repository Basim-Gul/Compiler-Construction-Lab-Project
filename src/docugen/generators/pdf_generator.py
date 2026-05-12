"""PDF generation for DocuGen."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF


def _prepare_text_for_pdf(value: str, chunk_size: int = 70) -> str:
    chunks: list[str] = []
    for word in value.split():
        if len(word) <= chunk_size:
            chunks.append(word)
            continue
        chunks.extend(
            word[chunk_start : chunk_start + chunk_size]
            for chunk_start in range(0, len(word), chunk_size)
        )
    return " ".join(part for part in chunks if part)


def _write_line(pdf: FPDF, text: str, height: int = 6) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, height, _prepare_text_for_pdf(text))


def _render_parameter_table(pdf: FPDF, parameters: list[dict]) -> None:
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(239, 246, 255)
    pdf.cell(55, 7, "Parameter", border=1, fill=True)
    pdf.cell(55, 7, "Type", border=1, fill=True)
    pdf.cell(80, 7, "Description", border=1, ln=True, fill=True)
    pdf.set_font("Helvetica", size=10)
    if not parameters:
        pdf.cell(190, 7, "No parameters.", border=1, ln=True)
        return
    for parameter in parameters:
        pdf.cell(55, 7, str(parameter.get("name", "")), border=1)
        pdf.cell(55, 7, str(parameter.get("annotation") or "untyped"), border=1)
        pdf.cell(80, 7, "-", border=1, ln=True)


def _render_function_card(pdf: FPDF, title: str, function: dict) -> None:
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(191, 219, 254)
    pdf.set_line_width(0.25)
    pdf.multi_cell(0, 8, "", border=1, fill=True)
    pdf.set_y(pdf.get_y() - 8)
    pdf.set_x(pdf.l_margin + 2)
    pdf.set_font("Helvetica", "B", 12)
    _write_line(pdf, f"{title}: {function['name']}", height=7)
    pdf.set_font("Courier", size=10)
    _write_line(pdf, f"def {function['name']}(... ) -> {function.get('returns') or 'None'}", height=6)
    pdf.set_font("Helvetica", size=10)
    decorators = function.get("decorators") or []
    if decorators:
        _write_line(pdf, f"Decorators: {', '.join(f'@{item}' for item in decorators)}")
    docstring = function.get("docstring") or {}
    _write_line(pdf, f"Docstring: {docstring.get('value', 'Not provided')}")
    _render_parameter_table(pdf, function.get("parameters", []))
    pdf.ln(2)


def generate_pdf(ir: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf = FPDF(format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.set_fill_color(30, 64, 175)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 14, "DocuGen Documentation", ln=True, fill=True)
    pdf.set_text_color(15, 23, 42)
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Table of Contents", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 6, "1. Modules and Functions", ln=True)
    pdf.cell(0, 6, "2. Classes and Methods", ln=True)
    pdf.cell(0, 6, "3. Semantic Warnings", ln=True)
    pdf.cell(0, 6, "4. Parser Errors", ln=True)

    pdf.ln(3)
    pdf.set_font("Helvetica", size=11)
    for module in ir.get("modules", []):
        pdf.set_font("Helvetica", "B", 14)
        _write_line(pdf, f"Module: {module['name']}", height=8)
        for function in module.get("functions", []):
            _render_function_card(pdf, "Function", function)
        for klass in module.get("classes", []):
            pdf.set_fill_color(239, 246, 255)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, f"Class: {klass['name']}", ln=True, fill=True)
            pdf.set_font("Helvetica", size=10)
            _write_line(pdf, f"Inherits: {', '.join(klass.get('bases') or []) or 'None'}")
            decorators = klass.get("decorators") or []
            if decorators:
                _write_line(pdf, f"Decorators: {', '.join(f'@{item}' for item in decorators)}")
            class_docstring = klass.get("docstring") or {}
            _write_line(pdf, f"Docstring: {class_docstring.get('value', 'Not provided')}")
            for method in klass.get("methods", []):
                _render_function_card(pdf, "Method", method)

    warnings = ir.get("semantic_warnings", [])
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.multi_cell(0, 8, "Semantic Warnings")
    pdf.set_font("Helvetica", size=11)
    if warnings:
        for warning in warnings:
            _write_line(pdf, f"- {warning}")
    else:
        _write_line(pdf, "No semantic warnings.")

    parser_errors = ir.get("parser_errors", [])
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.multi_cell(0, 8, "Parser Errors")
    pdf.set_font("Helvetica", size=11)
    if parser_errors:
        for parser_error in parser_errors:
            _write_line(pdf, f"- {parser_error}")
    else:
        _write_line(pdf, "No parser errors.")

    pdf.output(str(output_path))
