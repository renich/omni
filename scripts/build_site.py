#!/usr/bin/env python3
"""
Omni Static Site Generator
Builds a fast, lightweight, self-contained documentation site and code browser.
Supports light/dark theme, interactive language standard tabs, and Pygments syntax highlighting.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
import pygments
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter

STANDARDS = [
    {
        "id": "c23",
        "name": "C23",
        "title": "ISO/IEC 9899:2024 (C23)",
        "year": "2024",
        "file": "c/c23.c",
        "badge": "Modern Standard",
        "summary": "Full ISO C23 standard reference with standard attributes, extended #embed parameters, constexpr, nullptr, typeof, typeof_unqual, _BitInt, binary literals, and digit separators.",
        "flags": "-std=c23 -Wall -Wextra -pedantic -Werror -pthread -lm",
        "keywords": "59 / 59 keywords saturated",
        "features": [
            "Extended #embed with limit, prefix, suffix, and if_empty parameters",
            "Standard attributes ([[nodiscard]], [[maybe_unused]], [[reproducible]], [[unsequenced]], [[noreturn]])",
            "constexpr, bool/true/false, nullptr, typeof, typeof_unqual",
            "Bit-precise integers (_BitInt) with variable widths",
            "Binary literals (0b...) and single-quote digit separators",
            "Dual-Path Saturation Pattern for Annex F/H (DFP) and Annex G (Imaginary)",
            "Scalar state accumulator consuming all symbols without unused-variable warnings",
        ],
    },
    {
        "id": "c17",
        "name": "C17",
        "title": "ISO/IEC 9899:2018 (C17)",
        "year": "2018",
        "file": "c/c17.c",
        "badge": "Consolidation",
        "summary": "Technical defect-resolution edition of C11. Enforces strict __STDC_VERSION__ == 201710L and adopts direct atomic initialization following Defect Report 485 deprecation of ATOMIC_VAR_INIT.",
        "flags": "-std=c17 -Wall -Wextra -pedantic -Werror -pthread -lm",
        "keywords": "Full ISO C17 keyword saturation",
        "features": [
            "Fixed standard macro __STDC_VERSION__ == 201710L",
            "Atomic initialization differentiation via direct initialization (DR 485)",
            "Retains all C11 features (_Atomic, _Generic, _Static_assert, _Thread_local, _Alignas)",
            "Dual-Path Saturation Pattern for optional Annex G _Imaginary",
            "Scalar state accumulator consuming all declared scalars",
        ],
    },
    {
        "id": "c11",
        "name": "C11",
        "title": "ISO/IEC 9899:2011 (C11)",
        "year": "2011",
        "file": "c/c11.c",
        "badge": "Concurrency & Generics",
        "summary": "Major milestone introducing standardized multithreading, atomic operations, compile-time assertions, type-generic expressions, alignment queries, and unicode string literals.",
        "flags": "-std=c11 -Wall -Wextra -pedantic -Werror -pthread -lm",
        "keywords": "Full ISO C11 keyword saturation",
        "features": [
            "Atomics with stdatomic.h and memory order parameters (ATOMIC_VAR_INIT)",
            "Compile-time static assertions (_Static_assert)",
            "Type-generic selection expressions (_Generic)",
            "Thread-local storage duration (_Thread_local)",
            "Alignment specifiers (_Alignas) and queries (_Alignof)",
            "Anonymous structures and unions",
            "Unicode characters and string literals (u8, u, U, char16_t, char32_t)",
        ],
    },
    {
        "id": "c99",
        "name": "C99",
        "title": "ISO/IEC 9899:1999 (C99)",
        "year": "1999",
        "file": "c/c99.c",
        "badge": "Modernization",
        "summary": "Landmark modernization standard introducing mixed declarations, variable-length arrays, designated initializers, compound literals, flexible array members, complex arithmetic, and exact-width integer types.",
        "flags": "-std=c99 -Wall -Wextra -pedantic -Werror -lm",
        "keywords": "Full ISO C99 keyword saturation",
        "features": [
            "Mixed declarations and statements; for-loop index declarations",
            "Variable-length arrays (VLAs) and flexible array members",
            "Designated initializers and compound literals",
            "Native Boolean type (_Bool) via stdbool.h",
            "Exact-width integer types via stdint.h",
            "Complex arithmetic via complex.h",
            "inline functions and restrict pointer qualifiers",
            "Variadic macros and preprocessor __func__ identifier",
        ],
    },
    {
        "id": "c89",
        "name": "C89/C90",
        "title": "ANSI X3.159-1989 / ISO/IEC 9899:1990",
        "year": "1989",
        "file": "c/c89.c",
        "badge": "The Baseline",
        "summary": "The original standardized ANSI/ISO C compendium. Exercises the complete foundational grammar under strict declarations-before-statements ordering, exact 32 keywords, and classic K&R compatibility.",
        "flags": "-std=c89 -Wall -Wextra -pedantic -Werror -lm",
        "keywords": "Exact 32 ANSI C keywords saturated",
        "features": [
            "Strict declaration-before-statement ordering across all lexical blocks",
            "Exact 32 keywords defined in ANSI X3.159-1989",
            "Absence of trailing enum commas (strictly forbidden in C89)",
            "Variadic arguments via standard stdarg.h (sum_variadic)",
            "Non-local jumps (setjmp/longjmp) and pure ISO signal handling (SIGINT)",
            "Unbounded string manipulation demonstration (strcpy) with threat modeling",
            "Scalar state accumulator consuming all declared variables",
        ],
    },
]

def build_site(repo_root: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_lexer = CLexer()

    formatter_light = HtmlFormatter(style="github-light", nowrap=False, linenos="table", cssclass="highlight-light")
    formatter_dark = HtmlFormatter(style="github-dark", nowrap=False, linenos="table", cssclass="highlight-dark")

    css_light = formatter_light.get_style_defs(".highlight-light")
    css_dark = formatter_dark.get_style_defs(".highlight-dark")

    standards_data = []
    for item in STANDARDS:
        source_path = repo_root / item["file"]
        if not source_path.exists():
            print(f"Warning: {source_path} not found, skipping.")
            continue
        code_content = source_path.read_text(encoding="utf-8")
        line_count = len(code_content.splitlines())

        html_light = pygments.highlight(code_content, c_lexer, formatter_light)
        html_dark = pygments.highlight(code_content, c_lexer, formatter_dark)

        standards_data.append({
            **item,
            "line_count": line_count,
            "raw_code": code_content,
            "html_light": html_light,
            "html_dark": html_dark,
        })

    html_content = generate_html(standards_data, css_light, css_dark)
    output_file = output_dir / "index.html"
    output_file.write_text(html_content, encoding="utf-8")
    print(f"==> Omni site built successfully: {output_file} ({output_file.stat().st_size:,} bytes)")


def generate_html(standards: list[dict], css_light: str, css_dark: str) -> str:
    tabs_html = []
    panels_html = []

    for i, std in enumerate(standards):
        active_class = "active" if i == 0 else ""
        aria_selected = "true" if i == 0 else "false"
        tab_button = f"""
        <button class="std-tab {active_class}" role="tab" id="tab-{std['id']}" aria-selected="{aria_selected}" aria-controls="panel-{std['id']}" onclick="switchStandard('{std['id']}')">
            <span class="tab-name">{std['name']}</span>
            <span class="tab-badge">{std['year']}</span>
        </button>
        """
        tabs_html.append(tab_button)

        features_li = "".join(f"<li>{feat}</li>" for feat in std["features"])

        panel = f"""
        <div class="std-panel {active_class}" role="tabpanel" id="panel-{std['id']}" aria-labelledby="tab-{std['id']}">
            <div class="panel-meta">
                <div class="meta-header">
                    <div>
                        <span class="badge-pill">{std['badge']}</span>
                        <h2 class="meta-title">{std['title']}</h2>
                    </div>
                    <div class="meta-actions">
                        <button class="btn-copy" onclick="copyCode('{std['id']}')" title="Copy code to clipboard">
                            <svg class="icon-copy" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            <span id="copy-text-{std['id']}">Copy Code</span>
                        </button>
                        <a href="https://gitlab.com/renich/omni/-/blob/master/{std['file']}" target="_blank" rel="noopener" class="btn-source" title="View raw source on GitLab">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                            Source
                        </a>
                    </div>
                </div>
                <p class="meta-desc">{std['summary']}</p>
                <div class="meta-grid">
                    <div class="meta-card">
                        <span class="card-label">Verification Command</span>
                        <code class="cmd-code">{std['flags']}</code>
                    </div>
                    <div class="meta-card">
                        <span class="card-label">Metric</span>
                        <span class="card-value">{std['line_count']} lines &bull; {std['keywords']}</span>
                    </div>
                </div>
                <details class="features-details">
                    <summary>Standard Capabilities Showcase</summary>
                    <ul class="features-list">
                        {features_li}
                    </ul>
                </details>
            </div>

            <div class="code-container">
                <div class="code-view code-light">
                    {std['html_light']}
                </div>
                <div class="code-view code-dark">
                    {std['html_dark']}
                </div>
                <textarea id="raw-code-{std['id']}" style="display:none;" readonly>{std['raw_code']}</textarea>
            </div>
        </div>
        """
        panels_html.append(panel)

    tabs_str = "\n".join(tabs_html)
    panels_str = "\n".join(panels_html)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omni &mdash; Executable Language Compendiums</title>
    <meta name="description" content="The smallest piece of code that showcases the entirety of a programming language. Self-contained, zero-warning executable Rosetta stone.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&omega;</text></svg>">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <style>
        :root {{
            --font-mono: "JetBrains Mono", "Fira Code", "Cascadia Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            --brand-primary: #10b981;
            --brand-primary-hover: #059669;
            --code-bg-light: #ffffff;
            --code-bg-dark: #0d1117;
            --border-radius: 8px;
        }}

        body {{
            font-family: var(--font-sans);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}

        header.site-header {{
            border-bottom: 1px solid var(--pico-muted-border-color);
            padding: 1rem 0;
            background: var(--pico-background-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(8px);
        }}

        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: var(--pico-color);
            font-weight: 700;
            font-size: 1.35rem;
        }}

        .brand-symbol {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            background: var(--brand-primary);
            color: #ffffff;
            border-radius: 8px;
            font-size: 1.25rem;
            font-weight: 800;
        }}

        .nav-links {{
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }}

        .nav-link {{
            color: var(--pico-muted-color);
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.15s ease;
        }}

        .nav-link:hover {{
            color: var(--pico-color);
        }}

        .theme-toggle {{
            background: transparent;
            border: 1px solid var(--pico-muted-border-color);
            color: var(--pico-color);
            padding: 0.4rem 0.75rem;
            border-radius: var(--border-radius);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
        }}

        .hero {{
            max-width: 1200px;
            margin: 3rem auto 2rem auto;
            padding: 0 1.5rem;
            text-align: center;
        }}

        .hero h1 {{
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
        }}

        .hero-lead {{
            font-size: 1.25rem;
            color: var(--pico-muted-color);
            max-width: 780px;
            margin: 0 auto 2rem auto;
        }}

        .repo-mirrors {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }}

        .mirror-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.85rem;
            text-decoration: none;
            border: 1px solid var(--pico-muted-border-color);
            color: var(--pico-color);
            background: var(--pico-card-background-color);
            transition: all 0.2s ease;
        }}

        .mirror-pill:hover {{
            border-color: var(--brand-primary);
            color: var(--brand-primary);
            transform: translateY(-1px);
        }}

        .mirror-pill.primary {{
            border-color: #fc6d26;
            font-weight: 600;
        }}

        .main-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem 4rem 1.5rem;
        }}

        /* Standards navigation */
        .std-nav {{
            display: flex;
            gap: 0.5rem;
            border-bottom: 2px solid var(--pico-muted-border-color);
            margin-bottom: 1.5rem;
            overflow-x: auto;
            padding-bottom: 0.25rem;
        }}

        .std-tab {{
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            padding: 0.75rem 1.25rem;
            cursor: pointer;
            color: var(--pico-muted-color);
            font-weight: 600;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-radius: var(--border-radius) var(--border-radius) 0 0;
            transition: all 0.15s ease;
        }}

        .std-tab:hover {{
            color: var(--pico-color);
            background: var(--pico-card-background-color);
        }}

        .std-tab.active {{
            color: var(--brand-primary);
            border-bottom-color: var(--brand-primary);
            background: var(--pico-card-background-color);
        }}

        .tab-badge {{
            font-size: 0.75rem;
            padding: 0.15rem 0.45rem;
            border-radius: 12px;
            background: var(--pico-muted-border-color);
            color: var(--pico-color);
        }}

        /* Panel content */
        .std-panel {{
            display: none;
        }}

        .std-panel.active {{
            display: block;
        }}

        .panel-meta {{
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .meta-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }}

        .badge-pill {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--brand-primary);
            margin-bottom: 0.25rem;
        }}

        .meta-title {{
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
        }}

        .meta-actions {{
            display: flex;
            gap: 0.5rem;
        }}

        .btn-copy, .btn-source {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.4rem 0.8rem;
            font-size: 0.85rem;
            border-radius: var(--border-radius);
            text-decoration: none;
            cursor: pointer;
            font-weight: 500;
        }}

        .btn-copy {{
            background: var(--brand-primary);
            color: #ffffff;
            border: none;
            transition: background 0.15s ease;
        }}

        .btn-copy:hover {{
            background: var(--brand-primary-hover);
        }}

        .btn-source {{
            background: transparent;
            border: 1px solid var(--pico-muted-border-color);
            color: var(--pico-color);
        }}

        .btn-source:hover {{
            background: var(--pico-card-background-color);
        }}

        .meta-desc {{
            color: var(--pico-muted-color);
            margin-bottom: 1rem;
            font-size: 1rem;
        }}

        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }}

        .meta-card {{
            background: var(--pico-background-color);
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            border: 1px solid var(--pico-muted-border-color);
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .card-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 600;
            color: var(--pico-muted-color);
            letter-spacing: 0.05em;
        }}

        .card-value {{
            font-size: 0.95rem;
            font-weight: 600;
        }}

        .cmd-code {{
            font-family: var(--font-mono);
            font-size: 0.8rem;
            word-break: break-all;
            background: transparent;
            padding: 0;
            color: var(--brand-primary);
        }}

        .features-details {{
            border-top: 1px solid var(--pico-muted-border-color);
            padding-top: 0.75rem;
            margin-top: 0.75rem;
        }}

        .features-details summary {{
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--pico-color);
        }}

        .features-list {{
            margin: 0.75rem 0 0 0;
            padding-left: 1.5rem;
            font-size: 0.9rem;
            color: var(--pico-muted-color);
        }}

        .features-list li {{
            margin-bottom: 0.35rem;
        }}

        /* Code Browser */
        .code-container {{
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            overflow: hidden;
            font-family: var(--font-mono);
            font-size: 0.825rem;
            line-height: 1.45;
            position: relative;
        }}

        .code-view {{
            max-height: 650px;
            overflow-y: auto;
            overflow-x: auto;
        }}

        html[data-theme="dark"] .code-light {{ display: none; }}
        html[data-theme="dark"] .code-dark {{ display: block; }}
        html[data-theme="light"] .code-light {{ display: block; }}
        html[data-theme="light"] .code-dark {{ display: none; }}

        .highlight-light {{ background-color: var(--code-bg-light); }}
        .highlight-dark {{ background-color: var(--code-bg-dark); }}

        .code-container table.highlighttable {{
            margin: 0;
            border-collapse: collapse;
            width: 100%;
        }}

        .code-container td.linenos {{
            user-select: none;
            padding: 0.75rem 0.5rem 0.75rem 0.75rem;
            text-align: right;
            border-right: 1px solid var(--pico-muted-border-color);
            color: var(--pico-muted-color);
            opacity: 0.6;
            vertical-align: top;
            width: 45px;
        }}

        .code-container td.code {{
            padding: 0.75rem 1rem;
            vertical-align: top;
        }}

        .code-container pre {{
            margin: 0;
            background: transparent;
            padding: 0;
            border: none;
            overflow: visible;
        }}

        /* Explanatory Sections */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin: 3.5rem 0;
        }}

        .info-card {{
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
        }}

        .info-card h3 {{
            margin-top: 0;
            font-size: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .info-card p {{
            color: var(--pico-muted-color);
            font-size: 0.95rem;
            margin-bottom: 0;
        }}

        footer.site-footer {{
            border-top: 1px solid var(--pico-muted-border-color);
            padding: 2.5rem 0;
            text-align: center;
            font-size: 0.9rem;
            color: var(--pico-muted-color);
        }}

        footer a {{
            color: var(--brand-primary);
            text-decoration: none;
        }}

        /* Pygments CSS Rules */
        {css_light}
        {css_dark}

        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
            .meta-header {{ flex-direction: column; }}
            .meta-actions {{ width: 100%; }}
            .btn-copy, .btn-source {{ flex: 1; justify-content: center; }}
        }}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="nav-container">
            <a href="#" class="brand">
                <span class="brand-symbol">&omega;</span>
                <span>omni</span>
            </a>
            <div class="nav-links">
                <a href="#browse" class="nav-link">Browse Standards</a>
                <a href="#principles" class="nav-link">Architecture</a>
                <a href="https://gitlab.com/renich/omni" target="_blank" rel="noopener" class="nav-link">GitLab</a>
                <button class="theme-toggle" id="theme-btn" onclick="toggleTheme()" aria-label="Toggle theme">
                    <span id="theme-icon">&#9790;</span>
                    <span id="theme-text">Dark</span>
                </button>
            </div>
        </div>
    </header>

    <section class="hero">
        <h1>The Entirety of a Language</h1>
        <p class="hero-lead">
            The smallest piece of self-contained, executable code that showcases 100% of a programming language's grammar, keywords, types, and directives. Zero warnings under pedantic compiler flags.
        </p>
        <div class="repo-mirrors">
            <a href="https://gitlab.com/renich/omni" target="_blank" rel="noopener" class="mirror-pill primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 0 1-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 0 1 4.82 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0 1 18.6 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.51L23 13.45a.84.84 0 0 1-.35.94z"></path></svg>
                GitLab Upstream (Canonical)
            </a>
            <a href="https://github.com/renich/omni" target="_blank" rel="noopener" class="mirror-pill">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
                GitHub Mirror (SHA-1)
            </a>
            <a href="https://git.openlat.dev/renich/omni" target="_blank" rel="noopener" class="mirror-pill">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                OpenLat Mirror
            </a>
        </div>
    </section>

    <main class="main-content" id="browse">
        <nav class="std-nav" role="tablist" aria-label="Language standards">
            {tabs_str}
        </nav>

        {panels_str}

        <section class="info-grid" id="principles">
            <div class="info-card">
                <h3>The Scalar State Accumulator</h3>
                <p>
                    Rather than polluting code with hundreds of dead <code>(void)var;</code> suppression casts, Omni mathematically consumes every declared scalar into a single state hash. This forces the compiler's optimizer and semantic analyzer to evaluate all symbols while compiling cleanly under <code>-Wall -Wextra -Werror</code>.
                </p>
            </div>
            <div class="info-card">
                <h3>Dual-Path Saturation Pattern</h3>
                <p>
                    For optional language annexes (such as Decimal Floating Point or Imaginary numbers), Omni employs an active preprocessor branch for supporting compilers and an inactive token-preserving fallback for conformant compilers without DFP runtimes. 100% lexical saturation is achieved without breaking builds.
                </p>
            </div>
            <div class="info-card">
                <h3>Bidirectional Threat Modeling</h3>
                <p>
                    When demonstrating historically hazardous or memory-unsafe constructs (VLAs, non-local jumps, unbounded buffer copies), code is tagged inline with <code>[!SECURITY-NOTE: ID]</code> linked directly to the language's security matrix detailing CWE identifiers and hardened production alternatives.
                </p>
            </div>
        </section>

        <section class="info-card" style="text-align: center; margin-top: 2rem;">
            <h3>Join the Horizon &bull; Calling Contributors</h3>
            <p style="max-width: 680px; margin: 0.5rem auto 1.5rem auto;">
                Omni is expanding across modern systems programming languages. We are actively seeking canonical reference files for <strong>C++</strong> (C++98 to C++26), <strong>Zig</strong>, <strong>Crystal</strong>, <strong>Go</strong>, <strong>Rust</strong>, <strong>Python</strong>, and <strong>Bash</strong>.
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <a href="https://gitlab.com/renich/omni/-/blob/master/CONTRIBUTING.rst" target="_blank" rel="noopener" class="mirror-pill primary">
                    Read Contributing Guide
                </a>
                <a href="https://gitlab.com/renich/omni/-/blob/master/docs/process.rst" target="_blank" rel="noopener" class="mirror-pill">
                    Architecture Methodology
                </a>
                <a href="https://gitlab.com/renich/omni/-/blob/master/AGENTS.md" target="_blank" rel="noopener" class="mirror-pill">
                    AI Agent Directive
                </a>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <p>
            Omni &mdash; Maintained by <a href="https://evalinux.com" target="_blank" rel="noopener">R&eacute;nich Bon &Cacute;iri&cacute;</a> and contributors.
        </p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            Open Source under standard free software licensing. Canonical source on <a href="https://gitlab.com/renich/omni" target="_blank" rel="noopener">GitLab</a>.
        </p>
    </footer>

    <script>
        function switchStandard(stdId) {{
            document.querySelectorAll('.std-tab').forEach(tab => {{
                tab.classList.remove('active');
                tab.setAttribute('aria-selected', 'false');
            }});
            document.querySelectorAll('.std-panel').forEach(panel => {{
                panel.classList.remove('active');
            }});

            const selectedTab = document.getElementById('tab-' + stdId);
            const selectedPanel = document.getElementById('panel-' + stdId);

            if (selectedTab && selectedPanel) {{
                selectedTab.classList.add('active');
                selectedTab.setAttribute('aria-selected', 'true');
                selectedPanel.classList.add('active');
            }}
        }}

        function copyCode(stdId) {{
            const rawTextArea = document.getElementById('raw-code-' + stdId);
            const copyBtnText = document.getElementById('copy-text-' + stdId);
            if (!rawTextArea) return;

            navigator.clipboard.writeText(rawTextArea.value).then(() => {{
                const originalText = copyBtnText.textContent;
                copyBtnText.textContent = "Copied!";
                setTimeout(() => {{
                    copyBtnText.textContent = originalText;
                }}, 2000);
            }}).catch(err => {{
                console.error("Clipboard copy failed: ", err);
            }});
        }}

        function toggleTheme() {{
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('omni-theme', newTheme);
            updateThemeUI(newTheme);
        }}

        function updateThemeUI(theme) {{
            const icon = document.getElementById('theme-icon');
            const text = document.getElementById('theme-text');
            if (theme === 'dark') {{
                icon.innerHTML = '&#9790;';
                text.textContent = 'Dark';
            }} else {{
                icon.innerHTML = '&#9788;';
                text.textContent = 'Light';
            }}
        }}

        // Initialize saved theme or system preference
        (function() {{
            const savedTheme = localStorage.getItem('omni-theme');
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
            document.documentElement.setAttribute('data-theme', initialTheme);
            updateThemeUI(initialTheme);
        }})();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / "public"
    build_site(repo_root, output_dir)
