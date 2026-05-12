# DocuGen: An Automated Documentation Generation System

**Course:** Compiler Construction Lab (CSL-323)

DocuGen is an automated documentation generation system built on core Compiler Construction principles. The system accepts Python source code as input and applies a full compiler pipeline — including lexical analysis, syntax parsing, AST generation, and semantic analysis — to extract meaningful documentation artifacts from source code comments, docstrings, function signatures, and class definitions.

## Project Scope
The scope of this project spans the full compiler construction pipeline applied to documentation extraction — from lexical analysis of source files to formatted HTML/PDF output.

## Modules & Pipeline
1. Lexical Analyzer (Lexer)
2. Syntax Analyzer (Parser)
3. AST Generation
4. Semantic Analyzer
5. Symbol Table Management
6. Intermediate Code / IR Generation
7. Documentation Output Generation

*Initialized via GitHub Copilot.*

## Project Structure

```text
src/
├── ast/
├── generator/
├── lexer/
│   └── lexer.py
├── parser/
├── semantic/
└── main.py
tests/
└── sample.py
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Basic Lexer

Run the lexer against the provided sample file:

```bash
python src/main.py
```

Or provide a custom Python file:

```bash
python src/main.py path/to/file.py
```
