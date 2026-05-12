# 📚 DocuGen — Automated Documentation Generation System

> **Course:** Compiler Construction Lab (CSL-323) · Bahria University, Karachi Campus  
> **Team:** Abdul Rauf (091) · Basim Khurrum Gul (052) · Umais Wahab (095)

---

## 👋 What is DocuGen?

**DocuGen** is a tool that reads your Python source code and **automatically generates beautiful documentation** for you — no manual writing required!

It works like a mini-compiler: it scans your `.py` files, understands the code structure (functions, classes, docstrings, type hints), and then produces:

| Output | Description |
|--------|-------------|
| 🌐 **HTML page** | A styled, readable documentation website |
| 📄 **PDF file** | A printable documentation document |
| 🌳 **AST diagram** | A visual tree showing how your code is structured |
| 🗂️ **IR JSON** | A machine-readable summary of your code |

---

## 🔧 Prerequisites

Before you start, make sure you have the following installed on your computer:

1. **Python 3.9 or newer** — [Download here](https://www.python.org/downloads/)
   - Check your version: `python --version`
2. **pip** — usually installed with Python automatically
   - Check: `pip --version`
3. *(Optional)* **Graphviz** — needed to render the visual AST diagram as an image
   - [Download here](https://graphviz.org/download/) and make sure it's added to your system PATH

> 💡 **Tip for Windows users:** During Python installation, tick the *"Add Python to PATH"* checkbox.

---

## 📥 Installation

### Step 1 — Clone or download the repository

```bash
git clone https://github.com/Basim-Gul/Compiler-Construction-Lab-Project.git
cd Compiler-Construction-Lab-Project
```

### Step 2 — Install the required Python libraries

```bash
pip install -r requirements.txt
```

This installs:
- **PLY** — for lexical analysis and parsing
- **Jinja2** — for HTML template rendering
- **fpdf2** — for PDF generation
- **graphviz** — for AST visualization

> ⚠️ If `pip` is not found, try `pip3` instead.

---

## 🚀 How to Use DocuGen

### Option A — Run the quick demo (easiest way)

A ready-to-run demo script is included. It analyzes the sample Python file in `tests/sample.py` and saves all outputs to the `docs/` folder.

```bash
python test_run.py
```

You should see output like:

```
Generated outputs:
- ast: docs/ast.mmd
- ast_dot: docs/ast.dot
- ir: docs/ir.json
- html: docs/output.html
- pdf: docs/output.pdf
```

✅ Done! Open `docs/output.html` in your browser to see the documentation.

---

### Option B — Analyze your own Python file

Create a small Python script (e.g. `run_docugen.py`) in the project root:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from docugen import analyze_project

result = analyze_project(
    project_path="path/to/your_file.py",   # ← change this
    output_dir="docs",
    generate_html=True,
    generate_pdf=True,
    generate_ast=True,
    generate_ir=True,
)

print("Generated outputs:")
for key, value in result["outputs"].items():
    print(f"  {key}: {value}")
```

Then run it:

```bash
python run_docugen.py
```

---

### Option C — Analyze an entire project folder

Just point `project_path` at a directory instead of a single file:

```python
result = analyze_project(
    project_path="path/to/your_project/",  # ← folder with .py files
    output_dir="docs",
    generate_html=True,
    generate_pdf=True,
    generate_ast=True,
    generate_ir=True,
)
```

DocuGen will scan every `.py` file in the folder and combine them into one documentation output.

---

## 📂 Where Are the Outputs Saved?

After running DocuGen, check the `docs/` folder:

```
docs/
├── output.html   ← Open this in any web browser
├── output.pdf    ← Open with any PDF viewer
├── ast.mmd       ← Mermaid diagram source (AST)
├── ast.dot       ← Graphviz diagram source (AST)
└── ir.json       ← Intermediate Representation (JSON)
```

> 🖥️ To view `output.html`, just double-click it or drag it into a browser window.

---

## 🏗️ Project Structure

```
Compiler-Construction-Lab-Project/
├── src/
│   └── docugen/               ← Main Python package
│       ├── __init__.py        ← analyze_project() entry point
│       ├── lexer/             ← Lexical Analyzer (PLY)
│       ├── parser/            ← Syntax Analyzer & Parse Tree
│       ├── ast_engine/        ← AST node definitions
│       ├── semantic_analyzer/ ← Type checking & semantic validation
│       ├── symbol_table/      ← Scope & identifier tracking
│       ├── ir_generator/      ← JSON Intermediate Representation
│       ├── generators/        ← HTML & PDF output generators
│       └── visualization/     ← AST diagram builders
├── tests/
│   └── sample.py              ← Example Python file for testing
├── test_run.py                ← Quick demo runner
├── requirements.txt           ← Python dependencies
└── README.md                  ← This file
```

---

## ⚙️ Compiler Pipeline

DocuGen applies a full compiler pipeline to your code:

```
Your .py file
     │
     ▼
┌─────────────┐
│   Lexer     │  Breaks code into tokens (keywords, identifiers, etc.)
└──────┬──────┘
       ▼
┌─────────────┐
│   Parser    │  Builds a Parse Tree from tokens
└──────┬──────┘
       ▼
┌─────────────┐
│  AST Engine │  Converts Parse Tree → Abstract Syntax Tree
└──────┬──────┘
       ▼
┌──────────────────┐
│ Semantic Analyzer│  Checks types, missing docs, scope issues
└──────┬───────────┘
       ▼
┌──────────────┐
│ Symbol Table │  Tracks all identifiers and scopes
└──────┬───────┘
       ▼
┌──────────────┐
│ IR Generator │  Produces a JSON representation
└──────┬───────┘
       ▼
┌──────────────────────┐
│ HTML / PDF Generator │  Renders final documentation
└──────────────────────┘
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'ply'` | Run `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'docugen'` | Make sure you run scripts from the project root directory |
| PDF is empty or missing | Check that `fpdf2` is installed: `pip install fpdf2` |
| AST `.dot` file won't render to image | Install Graphviz from [graphviz.org](https://graphviz.org/download/) |

---

## 👨‍💻 Team & Module Assignments

| Member | Modules |
|--------|---------|
| **Abdul Rauf** (091) | Lexer, Parser, Error Handling |
| **Basim Khurrum Gul** (052) | AST Generation, Semantic Analyzer, Symbol Table |
| **Umais Wahab** (095) | IR Generation, HTML/PDF Output, Integration & Testing |

---

*Built with ❤️ for Compiler Construction Lab — Bahria University, Karachi*
