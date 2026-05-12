from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from docugen import analyze_project


if __name__ == "__main__":
    result = analyze_project(
        project_path=str(ROOT / "tests" / "sample.py"),
        output_dir=str(ROOT / "docs"),
        generate_html=True,
        generate_pdf=True,
        generate_ast=True,
        generate_ir=True,
    )
    print("Generated outputs:")
    for key, value in result["outputs"].items():
        print(f"- {key}: {value}")
