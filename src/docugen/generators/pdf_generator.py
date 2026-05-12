"""PDF generation for DocuGen."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF


def _sanitize_text(value: str, chunk_size: int = 70) -> str:
    chunks: list[str] = []
    for word in value.replace("\n", " ").split(" "):
        if len(word) <= chunk_size:
            chunks.append(word)
            continue
        chunks.extend(word[index : index + chunk_size] for index in range(0, len(word), chunk_size))
    return " ".join(part for part in chunks if part)


def _write_line(pdf: FPDF, text: str, height: int = 6) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, height, _sanitize_text(text))


def generate_pdf(ir: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "DocuGen Documentation", ln=True)

    pdf.set_font("Helvetica", size=12)
    for module in ir.get("modules", []):
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 13)
        _write_line(pdf, f"Module: {module['name']}", height=8)
        for function in module.get("functions", []):
            pdf.set_font("Helvetica", "B", 12)
            _write_line(pdf, f"Function: {function['name']}", height=7)
            pdf.set_font("Helvetica", size=11)
            _write_line(pdf, f"Returns: {function.get('returns') or 'None'}")
            docstring = function.get("docstring") or {}
            _write_line(pdf, f"Docstring: {docstring.get('value', 'Not provided')}")

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

    pdf.output(str(output_path))
