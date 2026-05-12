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
  <title>DocuGen Documentation</title>
  <script type="module" src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"></script>
  <style>
    @page { size: A4; margin: 16mm; }
    :root {
      --bg: #f8fafc;
      --surface: #ffffff;
      --text: #0f172a;
      --muted: #475569;
      --brand: #2563eb;
      --border: #dbeafe;
      --shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
    }
    * { box-sizing: border-box; }
    body { font-family: Inter, Segoe UI, Arial, sans-serif; margin: 0; background: var(--bg); color: var(--text); }
    .container { max-width: 1080px; margin: 0 auto; padding: 2rem 1.5rem 3rem; }
    .cover { background: linear-gradient(135deg, #1d4ed8, #0ea5e9); color: #fff; border-radius: 16px; padding: 2rem; box-shadow: var(--shadow); page-break-inside: avoid; }
    .cover h1 { margin: 0 0 0.5rem; font-size: 2rem; font-weight: 800; }
    .cover p { margin: 0; opacity: 0.95; }
    .toc, .section-card, .module-card, .class-card, .function-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; box-shadow: var(--shadow); margin-top: 1.1rem; padding: 1rem 1.1rem; page-break-inside: avoid; }
    .section-title { margin: 0 0 0.7rem; font-size: 1.12rem; color: #1e3a8a; }
    .module-title, .class-title, .function-title { margin: 0; font-size: 1.02rem; font-weight: 700; }
    .subtle { color: var(--muted); }
    .signature { background: #0f172a; color: #e2e8f0; border-radius: 10px; padding: 0.7rem 0.85rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin: 0.6rem 0; white-space: pre-wrap; }
    .badge { display: inline-block; margin-right: 0.35rem; margin-top: 0.3rem; padding: 0.16rem 0.5rem; border-radius: 999px; font-size: 0.76rem; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    table { width: 100%; border-collapse: collapse; margin-top: 0.4rem; }
    th, td { text-align: left; padding: 0.52rem 0.6rem; border-bottom: 1px solid #e2e8f0; font-size: 0.92rem; vertical-align: top; }
    th { background: #eff6ff; color: #1e3a8a; }
    ul { margin: 0.2rem 0 0; }
    .ast-tree { background: #111827; color: #d1d5db; border-radius: 10px; padding: 0.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; white-space: pre-wrap; }
  </style>
</head>
<body>
<div class="container">
  <section class="cover">
    <h1>DocuGen Documentation</h1>
    <p>Automated compiler-inspired API documentation generated from Python source code.</p>
  </section>

  <section class="toc">
    <h2 class="section-title">Table of Contents</h2>
    <ul>
      <li>Semantic Warnings</li>
      <li>Parser Errors</li>
      {% for module in ir.modules %}
      <li>Module: {{ module.name }}</li>
      {% endfor %}
      <li>AST Visualization</li>
    </ul>
  </section>

  <section class="section-card">
    <h2 class="section-title">Semantic Warnings</h2>
    {% if ir.semantic_warnings %}
      <ul>{% for warning in ir.semantic_warnings %}<li>{{ warning }}</li>{% endfor %}</ul>
    {% else %}
      <p class="subtle">No semantic warnings.</p>
    {% endif %}
  </section>

  <section class="section-card">
    <h2 class="section-title">Parser Errors</h2>
    {% if ir.parser_errors %}
      <ul>{% for error in ir.parser_errors %}<li>{{ error }}</li>{% endfor %}</ul>
    {% else %}
      <p class="subtle">No parser errors.</p>
    {% endif %}
  </section>

  {% for module in ir.modules %}
  <section class="module-card">
    <h2 class="module-title">Module: {{ module.name }}</h2>

    {% for function in module.functions %}
    <article class="function-card">
      <h3 class="function-title">Function: {{ function.name }}</h3>
      {% if function.decorators %}
        {% for decorator in function.decorators %}<span class="badge">@{{ decorator }}</span>{% endfor %}
      {% endif %}
      <div class="signature">def {{ function.name }}(... ) -> {{ function.returns or 'None' }}</div>
      <p><strong>Docstring:</strong> {{ function.docstring.value if function.docstring else 'Not provided' }}</p>
      <table>
        <thead>
          <tr><th>Parameter</th><th>Type</th><th>Description</th></tr>
        </thead>
        <tbody>
        {% for parameter in function.parameters %}
          <tr><td>{{ parameter.name }}</td><td>{{ parameter.annotation or 'untyped' }}</td><td>-</td></tr>
        {% endfor %}
        {% if not function.parameters %}
          <tr><td colspan="3" class="subtle">No parameters.</td></tr>
        {% endif %}
        </tbody>
      </table>
    </article>
    {% endfor %}

    {% for klass in module.classes %}
    <article class="class-card">
      <h3 class="class-title">Class: {{ klass.name }}</h3>
      {% if klass.decorators %}
        {% for decorator in klass.decorators %}<span class="badge">@{{ decorator }}</span>{% endfor %}
      {% endif %}
      <p><strong>Inherits:</strong> {{ klass.bases|join(', ') if klass.bases else 'None' }}</p>
      <p><strong>Docstring:</strong> {{ klass.docstring.value if klass.docstring else 'Not provided' }}</p>
      {% for method in klass.methods %}
      <article class="function-card">
        <h4 class="function-title">Method: {{ method.name }}</h4>
        {% if method.decorators %}
          {% for decorator in method.decorators %}<span class="badge">@{{ decorator }}</span>{% endfor %}
        {% endif %}
        <div class="signature">def {{ method.name }}(... ) -> {{ method.returns or 'None' }}</div>
        <p><strong>Docstring:</strong> {{ method.docstring.value if method.docstring else 'Not provided' }}</p>
        <table>
          <thead>
            <tr><th>Parameter</th><th>Type</th><th>Description</th></tr>
          </thead>
          <tbody>
          {% for parameter in method.parameters %}
            <tr><td>{{ parameter.name }}</td><td>{{ parameter.annotation or 'untyped' }}</td><td>-</td></tr>
          {% endfor %}
          {% if not method.parameters %}
            <tr><td colspan="3" class="subtle">No parameters.</td></tr>
          {% endif %}
          </tbody>
        </table>
      </article>
      {% endfor %}
      {% if not klass.methods %}
      <p class="subtle">No methods detected.</p>
      {% endif %}
    </article>
    {% endfor %}
  </section>
  {% endfor %}

  <section class="section-card">
    <h2 class="section-title">AST Visualization</h2>
    {% if mermaid_graph %}
      <div class="mermaid">{{ mermaid_graph }}</div>
      <h3 class="module-title" style="margin-top:0.8rem;">Text Tree</h3>
      <pre class="ast-tree">{{ mermaid_graph }}</pre>
    {% else %}
      <p class="subtle">AST generation disabled.</p>
    {% endif %}
  </section>
</div>
<script>mermaid.initialize({ startOnLoad: true, theme: 'default' });</script>
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
