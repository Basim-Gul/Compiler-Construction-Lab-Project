from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from docugen.generators.html_generator import generate_html
from docugen.lexer import tokenize
from docugen.parser import parse_source
from docugen.semantic_analyzer import analyze_semantics


SOURCE = """
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class PageRenderer(BaseRenderer):
    \"\"\"Render a page.\"\"\"
    @property
    def title(self) -> str:
        \"\"\"Page title.\"\"\"
        return "DocuGen"

    @classmethod
    def create(cls, pages: Dict[Tuple[int, int], Page] = {}) -> PageRenderer:
        \"\"\"Create renderer.\"\"\"
        return cls()

def helper(x: int, amount: float = 1.0) -> float:
    \"\"\"Helper function.\"\"\"
    data = [1, 2, 3]
    record = {"total": amount + x}
    return record["total"]
"""


class DocuGenPipelineTests(unittest.TestCase):
    def test_lexer_supports_python_symbols(self) -> None:
        tokens, errors = tokenize(SOURCE)
        self.assertEqual(errors, [])
        token_types = {token.type for token in tokens}
        self.assertTrue({"NUMBER", "STRING", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "AT", "ARROW"}.issubset(token_types))

    def test_parser_extracts_classes_methods_and_decorators(self) -> None:
        module, errors = parse_source(SOURCE, module_name="sample")
        self.assertEqual(errors, [])
        self.assertEqual(module.name, "sample")
        self.assertEqual(len(module.classes), 1)
        klass = module.classes[0]
        self.assertEqual(klass.name, "PageRenderer")
        self.assertEqual(klass.bases, ["BaseRenderer"])
        self.assertIn("dataclass", klass.decorators)
        methods = {method.name: method for method in klass.methods}
        self.assertIn("title", methods)
        self.assertIn("create", methods)
        self.assertIn("property", methods["title"].decorators)
        self.assertIn("classmethod", methods["create"].decorators)
        self.assertEqual(methods["create"].parameters[1].annotation, "Dict[Tuple[int, int], Page]")

    def test_semantic_self_cls_missing_annotation_ignored(self) -> None:
        module, _ = parse_source(SOURCE, module_name="sample")
        warnings = analyze_semantics(module)
        joined = " ".join(warnings)
        self.assertNotIn("Parameter 'self' in method 'PageRenderer.title' is missing a type annotation.", joined)
        self.assertNotIn("Parameter 'cls' in method 'PageRenderer.create' is missing a type annotation.", joined)

    def test_html_includes_modern_sections(self) -> None:
        module, _ = parse_source(SOURCE, module_name="sample")
        ir = {
            "modules": [module.to_dict()],
            "semantic_warnings": [],
            "parser_errors": [],
            "symbol_table": {},
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "out.html"
            generate_html(ir, "graph TD\nA-->B", output)
            html = output.read_text(encoding="utf-8")
            self.assertIn("DocuGen Documentation", html)
            self.assertIn("Table of Contents", html)
            self.assertIn("Parameter", html)
            self.assertIn("@page", html)
            self.assertIn("class-card", html)


if __name__ == "__main__":
    unittest.main()
