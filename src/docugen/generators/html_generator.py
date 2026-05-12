"""HTML generation for DocuGen."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Template

_TEMPLATE = Template(
    """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DocuGen Output</title>
  <script type="module" src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"></script>
  <style>
    body { font-family: Inter, Arial, sans-serif; margin: 0; padding: 0; background: #0f172a; color: #e2e8f0; }
    .container { max-width: 980px; margin: 0 auto; padding: 2rem; }
    .card { background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; }
    h1, h2, h3 { color: #f8fafc; }
    code { background: #1e293b; padding: 0.2rem 0.4rem; border-radius: 5px; }
    ul { margin-top: 0.3rem; }
  </style>
</head>
<body>
<div class="container">
  <h1>DocuGen Documentation</h1>
  <div class="card">
    <h2>Semantic Warnings</h2>
    {% if ir.semantic_warnings %}
      <ul>{% for warning in ir.semantic_warnings %}<li>{{ warning }}</li>{% endfor %}</ul>
    {% else %}
      <p>No semantic warnings.</p>
    {% endif %}
  </div>

  {% for module in ir.modules %}
  <div class="card">
    <h2>Module: {{ module.name }}</h2>
    {% for function in module.functions %}
      <h3>Function: <code>{{ function.name }}</code></h3>
      <p><strong>Returns:</strong> {{ function.returns or 'None' }}</p>
      <p><strong>Docstring:</strong> {{ function.docstring.value if function.docstring else 'Not provided' }}</p>
      <strong>Parameters</strong>
      <ul>
      {% for parameter in function.parameters %}
        <li><code>{{ parameter.name }}</code> : {{ parameter.annotation or 'untyped' }}</li>
      {% endfor %}
      </ul>
    {% endfor %}
  </div>
  {% endfor %}

  <div class="card">
    <h2>AST Visualization</h2>
    {% if mermaid_graph %}
      <div class="mermaid">{{ mermaid_graph }}</div>
    {% else %}
      <p>AST generation disabled.</p>
    {% endif %}
  </div>
</div>
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
</body>
</html>
""".strip()
)


def generate_html(ir: dict, mermaid_graph: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        _TEMPLATE.render(ir=ir, mermaid_graph=mermaid_graph),
        encoding="utf-8",
    )
