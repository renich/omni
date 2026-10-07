#!/usr/bin/python3
"""
Omni Static Site Generator
Builds a fast, lightweight, self-contained multi-language documentation site and code browser.
Features:
- Wide, responsive IDE-style File Explorer supporting arbitrary numbers of languages and editions
- Rendered HTML documentation for security matrices and guides, with interactive raw source toggle
- Interactive code browser with line numbers and Pygments syntax highlighting (friendly / dracula)
- Light/Dark theme switching with system preference detection
- Deep linking via URL hash routing
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
import pygments
from pygments.lexers import CLexer, TextLexer
from pygments.lexers.markup import RstLexer, MarkdownLexer
from pygments.formatters import HtmlFormatter

try:
    from docutils.core import publish_parts
    HAVE_DOCUTILS = True
except ImportError:
    HAVE_DOCUTILS = False

try:
    import markdown
    HAVE_MARKDOWN = True
except ImportError:
    HAVE_MARKDOWN = False

# Definition of verified languages and compendiums
C_STANDARDS = [
    {
        "id": "c-c23",
        "name": "c23.c",
        "tab_label": "C23",
        "title": "ISO/IEC 9899:2024 (C23)",
        "year": "2024",
        "file": "c/c23.c",
        "badge": "Modern Standard",
        "summary": "Full ISO C23 standard reference with standard attributes, extended #embed parameters, constexpr, nullptr, typeof, typeof_unqual, _BitInt, binary literals, and digit separators.",
        "flags": "-std=c23 -Wall -Wextra -pedantic -Werror -pthread -lm",
        "keywords": "59 / 59 keywords saturated",
        "security_anchors": ["SEC-VLA-01", "SEC-JMP-01", "SEC-BITFIELD-01", "SEC-ATOMIC-01"],
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
        "id": "c-c17",
        "name": "c17.c",
        "tab_label": "C17",
        "title": "ISO/IEC 9899:2018 (C17)",
        "year": "2018",
        "file": "c/c17.c",
        "badge": "Consolidation",
        "summary": "Technical defect-resolution edition of C11. Enforces strict __STDC_VERSION__ == 201710L and adopts direct atomic initialization following Defect Report 485 deprecation of ATOMIC_VAR_INIT.",
        "flags": "-std=c17 -Wall -Wextra -pedantic -Werror -pthread -lm",
        "keywords": "Full ISO C17 keyword saturation",
        "security_anchors": ["SEC-VLA-01", "SEC-JMP-01", "SEC-BITFIELD-01", "SEC-ATOMIC-01"],
        "features": [
            "Fixed standard macro __STDC_VERSION__ == 201710L",
            "Atomic initialization differentiation via direct initialization (DR 485)",
            "Retains all C11 features (_Atomic, _Generic, _Static_assert, _Thread_local, _Alignas)",
            "Dual-Path Saturation Pattern for optional Annex G _Imaginary",
            "Scalar state accumulator consuming all declared scalars",
        ],
    },
    {
        "id": "c-c11",
        "name": "c11.c",
        "tab_label": "C11",
        "title": "ISO/IEC 9899:2011 (C11)",
        "year": "2011",
        "file": "c/c11.c",
        "badge": "Concurrency & Generics",
        "summary": "Major milestone introducing standardized multithreading, atomic operations, compile-time assertions, type-generic expressions, alignment queries, and unicode string literals.",
        "flags": "-std=c11 -Wall -Wextra -pedantic -Werror -pthread -lm",
        "keywords": "Full ISO C11 keyword saturation",
        "security_anchors": ["SEC-VLA-01", "SEC-JMP-01", "SEC-BITFIELD-01", "SEC-ATOMIC-01"],
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
        "id": "c-c99",
        "name": "c99.c",
        "tab_label": "C99",
        "title": "ISO/IEC 9899:1999 (C99)",
        "year": "1999",
        "file": "c/c99.c",
        "badge": "Modernization",
        "summary": "Landmark modernization standard introducing mixed declarations, variable-length arrays, designated initializers, compound literals, flexible array members, complex arithmetic, and exact-width integer types.",
        "flags": "-std=c99 -Wall -Wextra -pedantic -Werror -lm",
        "keywords": "Full ISO C99 keyword saturation",
        "security_anchors": ["SEC-VLA-01", "SEC-JMP-01", "SEC-BITFIELD-01"],
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
        "id": "c-c89",
        "name": "c89.c",
        "tab_label": "C89/C90",
        "title": "ANSI X3.159-1989 / ISO/IEC 9899:1990",
        "year": "1989",
        "file": "c/c89.c",
        "badge": "The Baseline",
        "summary": "The original standardized ANSI/ISO C compendium. Exercises the complete foundational grammar under strict declarations-before-statements ordering, exact 32 keywords, and classic K&R compatibility.",
        "flags": "-std=c89 -Wall -Wextra -pedantic -Werror -lm",
        "keywords": "Exact 32 ANSI C keywords saturated",
        "security_anchors": ["SEC-JMP-01", "SEC-C89-UNBOUNDED-01", "SEC-BITFIELD-01"],
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

# Security matrix anchors for C
C_SECURITY_ANCHORS = [
    {
        "tag": "SEC-VLA-01",
        "standards": "C99, C11, C17, C23",
        "cwe": "CWE-400, CWE-770",
        "hazard": "Stack exhaustion / Denial of Service via dynamic runtime dimensions",
        "remediation": "Enforce bounded dynamic allocation (malloc) or fixed buffers with overflow checks",
    },
    {
        "tag": "SEC-JMP-01",
        "standards": "C89, C99, C11, C17, C23",
        "cwe": "CWE-398",
        "hazard": "Stack unwinding bypass, register clobbering, skipped resource cleanup",
        "remediation": "Replace setjmp/longjmp with structured return codes and explicit status propagation",
    },
    {
        "tag": "SEC-C89-UNBOUNDED-01",
        "standards": "C89",
        "cwe": "CWE-120",
        "hazard": "Classic buffer overflow via unbounded string utilities (strcpy, strcat)",
        "remediation": "Prohibit unbounded functions; enforce bounded copy or Annex K bounds-checking interfaces",
    },
    {
        "tag": "SEC-BITFIELD-01",
        "standards": "C89, C99, C11, C17, C23",
        "cwe": "CWE-198",
        "hazard": "Implementation-defined bitfield ordering, layout, and signedness ambiguity",
        "remediation": "Avoid bitfields for IPC/protocols; use explicit bitwise masking over fixed-width types",
    },
    {
        "tag": "SEC-ATOMIC-01",
        "standards": "C11, C17, C23",
        "cwe": "CWE-662",
        "hazard": "Data races and instruction reordering via relaxed memory orders",
        "remediation": "Default to sequential consistency (memory_order_seq_cst) unless formal models prove safety",
    },
]

# Language Horizon targets for community contributions
HORIZON_LANGUAGES = [
    {
        "id": "horizon-cpp",
        "name": "C++",
        "category": "Systems & Performance",
        "standard_org": "ISO/IEC 14882",
        "summary": "Multi-decade syntactic evolution spanning C++98, C++11, C++14, C++17, C++20, C++23, and upcoming C++26.",
        "target_files": [
            "cpp/cpp98.cpp", "cpp/cpp11.cpp", "cpp/cpp14.cpp",
            "cpp/cpp17.cpp", "cpp/cpp20.cpp", "cpp/cpp23.cpp",
            "cpp/security.rst", "cpp/README.rst",
        ],
        "target_flags": "-std=c++23 -Wall -Wextra -pedantic -Werror",
        "key_features": [
            "Templates, concepts, constraints, and compile-time evaluation (constexpr, consteval)",
            "Move semantics, smart pointers, RAII, and memory model",
            "Coroutines, ranges, modules, and explicit object parameters (deducing this)",
            "Required security.rst catalog for pointer arithmetic, reinterpret_cast, and lifetime hazards",
        ],
    },
    {
        "id": "horizon-zig",
        "name": "Zig",
        "category": "Systems & Tooling",
        "standard_org": "Zig Software Foundation",
        "summary": "No hidden control flow, compile-time metaprogramming (comptime), explicit memory allocators, and optimal binary sizing.",
        "target_files": [
            "zig/zig013.zig", "zig/zig014.zig",
            "zig/security.rst", "zig/README.rst",
        ],
        "target_flags": "zig build-exe -O ReleaseSafe",
        "key_features": [
            "Explicit allocators (std.mem.Allocator) and absence of global hidden heaps",
            "comptime reflection, error unions (!T), and tagged unions",
            "Struct-of-Arrays (std.MultiArrayList) and C ABI interoperability",
            "Required security.rst catalog for @ptrCast, @alignCast, and unmanaged memory",
        ],
    },
    {
        "id": "horizon-crystal",
        "name": "Crystal",
        "category": "Compiled & High-Level",
        "standard_org": "Manas.tech / Crystal Language",
        "summary": "Ruby-inspired elegance compiled down to native machine code via LLVM. Features static type inference, fibers, channels, and macro metaprogramming.",
        "target_files": [
            "crystal/crystal1.cr",
            "crystal/security.rst", "crystal/README.rst",
        ],
        "target_flags": "crystal build --release --warnings all",
        "key_features": [
            "Type unions and compile-time nil safety without runtime overhead",
            "CSP-style concurrency with light fibers, channels, and execution contexts",
            "Powerful compile-time AST macro expansion and native C library bindings (lib)",
            "Required security.rst catalog for Pointer(T), LibC unsafe calls, and fiber race conditions",
        ],
    },
    {
        "id": "horizon-go",
        "name": "Go",
        "category": "Cloud & Infrastructure",
        "standard_org": "Google / Go Authors",
        "summary": "Expressive simplicity, communicative concurrency with channels and goroutines, and first-class type parameters (generics).",
        "target_files": [
            "go/go122.go",
            "go/security.rst", "go/README.rst",
        ],
        "target_flags": "go build -race",
        "key_features": [
            "Goroutines, channels, and select statement concurrency",
            "Consumer-side interface contracts and type parameter generics",
            "Structured error handling and context propagation (context.Context)",
            "Required security.rst catalog for unsafe.Pointer and data race edge cases",
        ],
    },
    {
        "id": "horizon-rust",
        "name": "Rust",
        "category": "Memory-Safe Systems",
        "standard_org": "Rust Foundation",
        "summary": "Fearless concurrency, zero-cost abstractions, and strict compile-time borrow checker preventing memory safety defects.",
        "target_files": [
            "rust/rust2018.rs", "rust/rust2021.rs", "rust/rust2024.rs",
            "rust/security.rst", "rust/README.rst",
        ],
        "target_flags": "rustc --edition 2024 -D warnings",
        "key_features": [
            "Lifetimes, ownership, and borrow checking semantics",
            "Pattern matching, algebraic data types (enums), and trait systems",
            "Async/await and return position impl Trait in traits",
            "Required security.rst catalog for unsafe blocks and raw pointer dereferencing",
        ],
    },
    {
        "id": "horizon-python",
        "name": "Python",
        "category": "Dynamic & Scripting",
        "standard_org": "Python Software Foundation",
        "summary": "Rich syntactic grammar featuring structural pattern matching, comprehensive type annotations, and asynchronous coroutines.",
        "target_files": [
            "python/py313.py",
            "python/README.rst",
        ],
        "target_flags": "python3 -m py_compile",
        "key_features": [
            "Structural pattern matching (match / case) and union type operators (|)",
            "Type parameter syntax (PEP 695) and exception groups",
            "Async/await coroutines, comprehensions, and generators",
            "Scalar state consumer executing all defined functions and expressions",
        ],
    },
    {
        "id": "horizon-bash",
        "name": "Bash & POSIX",
        "category": "Shell & Systems",
        "standard_org": "IEEE Std 1003.1 / Free Software Foundation",
        "summary": "Pure POSIX shell standards alongside GNU Bash 5.x systems orchestration grammar.",
        "target_files": [
            "bash/bash5.bash", "sh/sh2024.sh",
            "bash/README.rst",
        ],
        "target_flags": "bash -n",
        "key_features": [
            "Associative arrays, parameter transformation, and arithmetic evaluation",
            "Process substitutions, coprocesses, and safe execution headers (set -euo pipefail)",
            "Strict POSIX compliance without non-standard extensions in sh/",
            "Required security.rst catalog for word splitting, glob expansion, and eval hazards",
        ],
    },
]

# Global documentation files
GLOBAL_DOCS = [
    {
        "id": "doc-standards",
        "name": "standards.rst",
        "title": "Language Standards and Roadmap",
        "file": "docs/standards.rst",
        "category": "Roadmap",
        "summary": "Comprehensive matrix of verified language editions, toolchain baselines, and prospective target horizons.",
    },
    {
        "id": "doc-architecture",
        "name": "architecture.rst",
        "title": "Repository Architecture Guide",
        "file": "docs/architecture.rst",
        "category": "Architecture",
        "summary": "Structural design, directory layout conventions, and single-file self-containment invariants.",
    },
    {
        "id": "doc-process",
        "name": "process.rst",
        "title": "Compendium Creation Process",
        "file": "docs/process.rst",
        "category": "Methodology",
        "summary": "The 6-phase engineering lifecycle for authoring, verifying, and maintaining omni language reference files.",
    },
    {
        "id": "doc-contributing",
        "name": "CONTRIBUTING.rst",
        "title": "Contributing Guidelines",
        "file": "CONTRIBUTING.rst",
        "category": "Governance",
        "summary": "Contribution requirements, workflow steps, submission checklist, and multi-platform channels.",
    },
    {
        "id": "doc-agents",
        "name": "AGENTS.md",
        "title": "Omni AI Agent Directive",
        "file": "AGENTS.md",
        "category": "AI Directives",
        "summary": "Non-negotiable invariants, scalar accumulator rules, and anti-hallucination guardrails for autonomous AI coding agents.",
    },
]


def get_lexer_for_file(filepath: str):
    if filepath.endswith(".c"):
        return CLexer()
    elif filepath.endswith(".rst"):
        return RstLexer()
    elif filepath.endswith(".md"):
        return MarkdownLexer()
    return TextLexer()


def render_doc_html(content: str, filepath: str) -> str:
    """Renders documentation (RST or Markdown) to HTML fragment."""
    if filepath.endswith(".rst") and HAVE_DOCUTILS:
        try:
            parts = publish_parts(content, writer_name="html5", settings_overrides={"report_level": 5})
            return parts.get("fragment", "")
        except Exception as e:
            return f"<p class='error'>Documentation render warning: {e}</p>"
    elif filepath.endswith(".md") and HAVE_MARKDOWN:
        try:
            return markdown.markdown(content, extensions=["tables", "fenced_code"])
        except Exception as e:
            return f"<p class='error'>Markdown render warning: {e}</p>"
    return ""


def highlight_file(filepath: Path, formatter_light: HtmlFormatter, formatter_dark: HtmlFormatter) -> tuple[str, str, int, str, str]:
    if not filepath.exists():
        return ("", "", 0, "", "")
    content = filepath.read_text(encoding="utf-8")
    lines = len(content.splitlines())
    lexer = get_lexer_for_file(str(filepath))
    html_light = pygments.highlight(content, lexer, formatter_light)
    html_dark = pygments.highlight(content, lexer, formatter_dark)
    rendered_doc = render_doc_html(content, str(filepath))
    return (html_light, html_dark, lines, content, rendered_doc)


def build_site(repo_root: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy assets into output directory
    assets_src = repo_root / "assets"
    assets_dst = output_dir / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)
    if assets_src.exists():
        for asset in assets_src.glob("*"):
            if asset.is_file():
                (assets_dst / asset.name).write_bytes(asset.read_bytes())

    formatter_light = HtmlFormatter(style="friendly", nowrap=False, linenos="table", cssclass="highlight-light")
    formatter_dark = HtmlFormatter(style="dracula", nowrap=False, linenos="table", cssclass="highlight-dark")

    css_light = formatter_light.get_style_defs(".highlight-light")
    css_dark = formatter_dark.get_style_defs(".highlight-dark")

    # 1. Process C standards
    processed_c_standards = []
    for item in C_STANDARDS:
        src = repo_root / item["file"]
        h_light, h_dark, lines, raw, _ = highlight_file(src, formatter_light, formatter_dark)
        processed_c_standards.append({
            **item,
            "line_count": lines,
            "html_light": h_light,
            "html_dark": h_dark,
            "raw_code": raw,
        })

    # 2. Process C security and documentation
    c_sec_path = repo_root / "c/security.rst"
    c_sec_light, c_sec_dark, c_sec_lines, c_sec_raw, c_sec_rendered = highlight_file(c_sec_path, formatter_light, formatter_dark)
    c_security_data = {
        "id": "c-security",
        "name": "security.rst",
        "title": "C Language Security and Hazardous Feature Matrix",
        "file": "c/security.rst",
        "line_count": c_sec_lines,
        "html_light": c_sec_light,
        "html_dark": c_sec_dark,
        "rendered_doc": c_sec_rendered,
        "raw_code": c_sec_raw,
        "anchors": C_SECURITY_ANCHORS,
    }

    c_readme_path = repo_root / "c/README.rst"
    c_readme_light, c_readme_dark, c_readme_lines, c_readme_raw, c_readme_rendered = highlight_file(c_readme_path, formatter_light, formatter_dark)
    c_readme_data = {
        "id": "c-readme",
        "name": "README.rst",
        "title": "C Reference Implementations and Standards Matrix",
        "file": "c/README.rst",
        "line_count": c_readme_lines,
        "html_light": c_readme_light,
        "html_dark": c_readme_dark,
        "rendered_doc": c_readme_rendered,
        "raw_code": c_readme_raw,
    }

    # 3. Process Global Documentation
    processed_global_docs = []
    for doc in GLOBAL_DOCS:
        doc_src = repo_root / doc["file"]
        h_light, h_dark, lines, raw, rendered = highlight_file(doc_src, formatter_light, formatter_dark)
        processed_global_docs.append({
            **doc,
            "line_count": lines,
            "html_light": h_light,
            "html_dark": h_dark,
            "rendered_doc": rendered,
            "raw_code": raw,
        })

    html_content = generate_html(
        c_standards=processed_c_standards,
        c_security=c_security_data,
        c_readme=c_readme_data,
        horizon_languages=HORIZON_LANGUAGES,
        global_docs=processed_global_docs,
        css_light=css_light,
        css_dark=css_dark,
    )

    output_file = output_dir / "index.html"
    output_file.write_text(html_content, encoding="utf-8")
    print(f"==> Omni site built successfully: {output_file} ({output_file.stat().st_size:,} bytes)")


def generate_html(
    c_standards: list[dict],
    c_security: dict,
    c_readme: dict,
    horizon_languages: list[dict],
    global_docs: list[dict],
    css_light: str,
    css_dark: str,
) -> str:
    # Sidebar tree generation
    c_items_html = []
    for std in c_standards:
        c_items_html.append(f"""
        <button class="nav-tree-item" id="btn-{std['id']}" onclick="switchView('{std['id']}')">
            <span class="file-icon std-icon">&lambda;</span>
            <span class="file-name">{std['name']}</span>
            <span class="file-badge">{std['year']}</span>
        </button>
        """)

    c_items_html.append(f"""
    <button class="nav-tree-item nav-security-item" id="btn-{c_security['id']}" onclick="switchView('{c_security['id']}')">
        <span class="file-icon sec-icon">&#128737;</span>
        <span class="file-name">{c_security['name']}</span>
        <span class="file-badge sec-badge">Threat Model</span>
    </button>
    <button class="nav-tree-item" id="btn-{c_readme['id']}" onclick="switchView('{c_readme['id']}')">
        <span class="file-icon doc-icon">&#128196;</span>
        <span class="file-name">{c_readme['name']}</span>
        <span class="file-badge">Overview</span>
    </button>
    """)
    c_tree_str = "\n".join(c_items_html)

    horizon_items_html = []
    for h in horizon_languages:
        horizon_items_html.append(f"""
        <button class="nav-tree-item horizon-item" id="btn-{h['id']}" onclick="switchView('{h['id']}')">
            <span class="file-icon horizon-icon">&#9671;</span>
            <span class="file-name">{h['name']}</span>
            <span class="file-badge horizon-badge">Planned</span>
        </button>
        """)
    horizon_tree_str = "\n".join(horizon_items_html)

    docs_items_html = []
    for d in global_docs:
        docs_items_html.append(f"""
        <button class="nav-tree-item" id="btn-{d['id']}" onclick="switchView('{d['id']}')">
            <span class="file-icon doc-icon">&#128220;</span>
            <span class="file-name">{d['name']}</span>
            <span class="file-badge">{d['category']}</span>
        </button>
        """)
    docs_tree_str = "\n".join(docs_items_html)

    # Panels generation
    panels_html = []

    # 1. C Standard Panels (Code Compendiums)
    for std in c_standards:
        features_li = "".join(f"<li>{feat}</li>" for feat in std["features"])
        anchors_pills = "".join(
            f'<button class="anchor-pill" onclick="switchView(\'c-security\')">{anchor}</button> '
            for anchor in std.get("security_anchors", [])
        )

        panel = f"""
        <div class="view-panel" id="panel-{std['id']}">
            <div class="panel-meta">
                <div class="meta-header">
                    <div>
                        <div class="meta-breadcrumbs">
                            <span class="crumb">omni</span>
                            <span class="crumb-sep">/</span>
                            <span class="crumb">c</span>
                            <span class="crumb-sep">/</span>
                            <span class="crumb current">{std['name']}</span>
                            <span class="badge-pill">{std['badge']}</span>
                        </div>
                        <h2 class="meta-title">{std['title']}</h2>
                    </div>
                    <div class="meta-actions">
                        <button class="btn-action btn-copy" onclick="copyContent('{std['id']}')" title="Copy code">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            <span id="copy-text-{std['id']}">Copy</span>
                        </button>
                        <a href="https://gitlab.com/renich/omni/-/blob/master/{std['file']}" target="_blank" rel="noopener" class="btn-action btn-link">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                            GitLab
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
                        <span class="card-label">Lexical Metrics</span>
                        <span class="card-value">{std['line_count']} lines &bull; {std['keywords']}</span>
                    </div>
                    <div class="meta-card">
                        <span class="card-label">Threat Model Anchors</span>
                        <div class="anchors-container">
                            {anchors_pills}
                        </div>
                    </div>
                </div>
                <details class="features-details">
                    <summary>Standard Capabilities Showcase ({len(std['features'])} items)</summary>
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
                <textarea id="raw-{std['id']}" style="display:none;" readonly>{std['raw_code']}</textarea>
            </div>
        </div>
        """
        panels_html.append(panel)

    # 2. C Security Threat Model Panel (Formatted Document + Raw Toggle)
    sec_rows = "".join(f"""
    <tr>
        <td><code class="anchor-code">{anchor['tag']}</code></td>
        <td>{anchor['standards']}</td>
        <td>{anchor['hazard']} <br><small class="cwe-tag">{anchor['cwe']}</small></td>
        <td>{anchor['remediation']}</td>
    </tr>
    """ for anchor in c_security["anchors"])

    sec_panel = f"""
    <div class="view-panel" id="panel-{c_security['id']}">
        <div class="panel-meta security-banner">
            <div class="meta-header">
                <div>
                    <div class="meta-breadcrumbs">
                        <span class="crumb">omni</span>
                        <span class="crumb-sep">/</span>
                        <span class="crumb">c</span>
                        <span class="crumb-sep">/</span>
                        <span class="crumb current">{c_security['name']}</span>
                        <span class="badge-pill sec-pill">Security &bull; Threat Catalog</span>
                    </div>
                    <h2 class="meta-title">&#128737; {c_security['title']}</h2>
                </div>
                <div class="meta-actions">
                    <div class="doc-view-toggle">
                        <button class="btn-toggle active" id="btn-mode-doc-{c_security['id']}" onclick="setDocMode('{c_security['id']}', 'doc')">Formatted Document</button>
                        <button class="btn-toggle" id="btn-mode-raw-{c_security['id']}" onclick="setDocMode('{c_security['id']}', 'raw')">Raw RST Source</button>
                    </div>
                    <button class="btn-action btn-copy" onclick="copyContent('{c_security['id']}')">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <span id="copy-text-{c_security['id']}">Copy</span>
                    </button>
                    <a href="https://gitlab.com/renich/omni/-/blob/master/{c_security['file']}" target="_blank" rel="noopener" class="btn-action btn-link">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        GitLab
                    </a>
                </div>
            </div>
            <p class="meta-desc">
                The <code>omni</code> C suite intentionally exercises historical, implementation-defined, and memory-hazardous constructs to achieve 100% grammar saturation. This threat model catalogs inline security anchors (<code>[!SECURITY-NOTE: ID]</code>), mapping them to formal CWE classifications and production mitigations.
            </p>

            <div class="security-table-wrapper">
                <table class="sec-matrix-table">
                    <thead>
                        <tr>
                            <th>Anchor Tag</th>
                            <th>Standards</th>
                            <th>Vulnerability &amp; CWE</th>
                            <th>Defensive Mitigation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sec_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Rendered Document View -->
        <div class="doc-rendered-container active" id="doc-rendered-{c_security['id']}">
            <article class="doc-article">
                {c_security['rendered_doc']}
            </article>
        </div>

        <!-- Raw RST Source View -->
        <div class="code-container doc-raw-container" id="doc-raw-{c_security['id']}">
            <div class="code-view code-light">
                {c_security['html_light']}
            </div>
            <div class="code-view code-dark">
                {c_security['html_dark']}
            </div>
        </div>
        <textarea id="raw-{c_security['id']}" style="display:none;" readonly>{c_security['raw_code']}</textarea>
    </div>
    """
    panels_html.append(sec_panel)

    # 3. C README Panel (Formatted Document + Raw Toggle)
    readme_panel = f"""
    <div class="view-panel" id="panel-{c_readme['id']}">
        <div class="panel-meta">
            <div class="meta-header">
                <div>
                    <div class="meta-breadcrumbs">
                        <span class="crumb">omni</span>
                        <span class="crumb-sep">/</span>
                        <span class="crumb">c</span>
                        <span class="crumb-sep">/</span>
                        <span class="crumb current">{c_readme['name']}</span>
                        <span class="badge-pill">Language Guide</span>
                    </div>
                    <h2 class="meta-title">{c_readme['title']}</h2>
                </div>
                <div class="meta-actions">
                    <div class="doc-view-toggle">
                        <button class="btn-toggle active" id="btn-mode-doc-{c_readme['id']}" onclick="setDocMode('{c_readme['id']}', 'doc')">Formatted Document</button>
                        <button class="btn-toggle" id="btn-mode-raw-{c_readme['id']}" onclick="setDocMode('{c_readme['id']}', 'raw')">Raw RST Source</button>
                    </div>
                    <button class="btn-action btn-copy" onclick="copyContent('{c_readme['id']}')">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <span id="copy-text-{c_readme['id']}">Copy</span>
                    </button>
                    <a href="https://gitlab.com/renich/omni/-/blob/master/{c_readme['file']}" target="_blank" rel="noopener" class="btn-action btn-link">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        GitLab
                    </a>
                </div>
            </div>
            <p class="meta-desc">
                C Language reference suite overview, compiler baselines, enforced warning flags, and per-standard distinguishing features.
            </p>
        </div>

        <div class="doc-rendered-container active" id="doc-rendered-{c_readme['id']}">
            <article class="doc-article">
                {c_readme['rendered_doc']}
            </article>
        </div>

        <div class="code-container doc-raw-container" id="doc-raw-{c_readme['id']}">
            <div class="code-view code-light">
                {c_readme['html_light']}
            </div>
            <div class="code-view code-dark">
                {c_readme['html_dark']}
            </div>
        </div>
        <textarea id="raw-{c_readme['id']}" style="display:none;" readonly>{c_readme['raw_code']}</textarea>
    </div>
    """
    panels_html.append(readme_panel)

    # 4. Global Docs Panels (Formatted Document + Raw Toggle)
    for doc in global_docs:
        doc_panel = f"""
        <div class="view-panel" id="panel-{doc['id']}">
            <div class="panel-meta">
                <div class="meta-header">
                    <div>
                        <div class="meta-breadcrumbs">
                            <span class="crumb">omni</span>
                            <span class="crumb-sep">/</span>
                            <span class="crumb">docs</span>
                            <span class="crumb-sep">/</span>
                            <span class="crumb current">{doc['name']}</span>
                            <span class="badge-pill">{doc['category']}</span>
                        </div>
                        <h2 class="meta-title">{doc['title']}</h2>
                    </div>
                    <div class="meta-actions">
                        <div class="doc-view-toggle">
                            <button class="btn-toggle active" id="btn-mode-doc-{doc['id']}" onclick="setDocMode('{doc['id']}', 'doc')">Formatted Document</button>
                            <button class="btn-toggle" id="btn-mode-raw-{doc['id']}" onclick="setDocMode('{doc['id']}', 'raw')">Raw Source</button>
                        </div>
                        <button class="btn-action btn-copy" onclick="copyContent('{doc['id']}')">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            <span id="copy-text-{doc['id']}">Copy</span>
                        </button>
                        <a href="https://gitlab.com/renich/omni/-/blob/master/{doc['file']}" target="_blank" rel="noopener" class="btn-action btn-link">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                            GitLab
                        </a>
                    </div>
                </div>
                <p class="meta-desc">{doc['summary']}</p>
                <div class="meta-grid">
                    <div class="meta-card">
                        <span class="card-label">File Path</span>
                        <code class="cmd-code">{doc['file']}</code>
                    </div>
                    <div class="meta-card">
                        <span class="card-label">Document Size</span>
                        <span class="card-value">{doc['line_count']} lines</span>
                    </div>
                </div>
            </div>

            <div class="doc-rendered-container active" id="doc-rendered-{doc['id']}">
                <article class="doc-article">
                    {doc['rendered_doc']}
                </article>
            </div>

            <div class="code-container doc-raw-container" id="doc-raw-{doc['id']}">
                <div class="code-view code-light">
                    {doc['html_light']}
                </div>
                <div class="code-view code-dark">
                    {doc['html_dark']}
                </div>
            </div>
            <textarea id="raw-{doc['id']}" style="display:none;" readonly>{doc['raw_code']}</textarea>
        </div>
        """
        panels_html.append(doc_panel)

    # 5. Horizon Language Blueprint Panels
    for h in horizon_languages:
        target_files_li = "".join(f"<li><code>{f}</code></li>" for f in h["target_files"])
        features_li = "".join(f"<li>{feat}</li>" for feat in h["key_features"])

        horizon_panel = f"""
        <div class="view-panel" id="panel-{h['id']}">
            <div class="panel-meta horizon-hero-card">
                <div class="meta-header">
                    <div>
                        <div class="meta-breadcrumbs">
                            <span class="crumb">omni</span>
                            <span class="crumb-sep">/</span>
                            <span class="crumb">horizon</span>
                            <span class="crumb-sep">/</span>
                            <span class="crumb current">{h['name']}</span>
                            <span class="badge-pill horizon-pill">Roadmap Target</span>
                        </div>
                        <h2 class="meta-title">&#9671; {h['name']} Target Specification</h2>
                    </div>
                    <div class="meta-actions">
                        <a href="https://gitlab.com/renich/omni/-/blob/master/CONTRIBUTING.rst" target="_blank" rel="noopener" class="btn-action btn-contribute">
                            Contribute {h['name']}
                        </a>
                    </div>
                </div>
                <p class="meta-desc">{h['summary']}</p>

                <div class="meta-grid">
                    <div class="meta-card">
                        <span class="card-label">Standard Body</span>
                        <span class="card-value">{h['standard_org']}</span>
                    </div>
                    <div class="meta-card">
                        <span class="card-label">Target Compiler Flags</span>
                        <code class="cmd-code">{h['target_flags']}</code>
                    </div>
                    <div class="meta-card">
                        <span class="card-label">Required Security Catalog</span>
                        <span class="card-value"><code>{h['name'].lower()}/security.rst</code> (Mandatory)</span>
                    </div>
                </div>

                <div class="horizon-blueprint-grid">
                    <div class="blueprint-section">
                        <h3>Planned Reference Files</h3>
                        <ul class="blueprint-list">
                            {target_files_li}
                        </ul>
                    </div>
                    <div class="blueprint-section">
                        <h3>Language Features to Saturate</h3>
                        <ul class="blueprint-list">
                            {features_li}
                        </ul>
                    </div>
                </div>

                <div class="horizon-cta">
                    <h3>Ready to Author the {h['name']} Compendium?</h3>
                    <p>
                        Review the 6-phase engineering lifecycle in the 
                        <button class="text-link-btn" onclick="switchView('doc-process')">Compendium Creation Process</button>
                        and check out the
                        <button class="text-link-btn" onclick="switchView('doc-contributing')">Contributing Guide</button>.
                    </p>
                </div>
            </div>
        </div>
        """
        panels_html.append(horizon_panel)

    panels_str = "\n".join(panels_html)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omni &mdash; Executable Language Compendiums</title>
    <meta name="description" content="The smallest piece of code that showcases the entirety of a programming language. Self-contained, zero-warning executable Rosetta stone with threat modeling.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&omega;</text></svg>">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <style>
        :root {{
            --font-mono: "JetBrains Mono", "Fira Code", "Cascadia Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            --brand-primary: #10b981;
            --brand-primary-hover: #059669;
            --brand-sec: #e11d48;
            --brand-sec-hover: #be123c;
            --brand-horizon: #8b5cf6;
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
            padding: 0.85rem 0;
            background: var(--pico-background-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(8px);
        }}

        /* Fluid Wide Containers */
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 100%;
            margin: 0;
            padding: 0 2rem;
            box-sizing: border-box;
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
            width: 32px;
            height: 32px;
            background: var(--brand-primary);
            color: #ffffff;
            border-radius: 8px;
            font-size: 1.2rem;
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
            padding: 0.35rem 0.7rem;
            border-radius: var(--border-radius);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
        }}

        .hero {{
            width: 100%;
            max-width: 100%;
            margin: 2rem 0 1.25rem 0;
            padding: 0 2rem;
            text-align: center;
            box-sizing: border-box;
        }}

        .hero h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.75rem;
        }}

        .hero-lead {{
            font-size: 1.15rem;
            color: var(--pico-muted-color);
            max-width: 900px;
            margin: 0 auto 1.5rem auto;
        }}

        .repo-mirrors {{
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }}

        .mirror-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.825rem;
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

        .mirror-pill.donate {{
            border-color: #f6c915;
            color: #d97706;
            font-weight: 600;
        }}

        /* Wide Fluid IDE-Style Layout */
        .explorer-layout {{
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 2rem;
            align-items: start;
            width: 100%;
            max-width: 100%;
            margin: 0;
            padding: 0 2rem 4rem 2rem;
            box-sizing: border-box;
        }}

        @media (min-width: 1920px) {{
            .explorer-layout {{
                grid-template-columns: 370px 1fr;
                padding: 0 3rem 4rem 3rem;
            }}
            .nav-container, .hero {{
                padding: 0 3rem;
            }}
        }}

        /* Explorer Sidebar */
        .explorer-sidebar {{
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 1.15rem;
            position: sticky;
            top: 4.8rem;
            max-height: calc(100vh - 6rem);
            overflow-y: auto;
        }}

        .sidebar-section {{
            margin-bottom: 1.25rem;
        }}

        .sidebar-section:last-child {{
            margin-bottom: 0;
        }}

        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--pico-muted-color);
            font-weight: 700;
            padding: 0.25rem 0.5rem 0.5rem 0.5rem;
            border-bottom: 1px solid var(--pico-muted-border-color);
            margin-bottom: 0.5rem;
        }}

        .status-dot {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--brand-primary);
            margin-right: 0.35rem;
        }}

        .status-dot.horizon {{
            background: var(--brand-horizon);
        }}

        .nav-tree-item {{
            display: flex;
            align-items: center;
            width: 100%;
            background: transparent;
            border: none;
            border-radius: 6px;
            padding: 0.45rem 0.65rem;
            cursor: pointer;
            color: var(--pico-color);
            font-size: 0.875rem;
            font-weight: 500;
            text-align: left;
            transition: all 0.15s ease;
            gap: 0.6rem;
            margin-bottom: 0.2rem;
            box-sizing: border-box;
        }}

        .nav-tree-item:hover {{
            background: var(--pico-muted-border-color);
        }}

        .nav-tree-item.active {{
            background: var(--brand-primary);
            color: #ffffff;
            font-weight: 600;
        }}

        .nav-tree-item.active .file-badge {{
            background: rgba(0, 0, 0, 0.25);
            color: #ffffff;
        }}

        .nav-tree-item.active .file-icon {{
            color: #ffffff;
        }}

        .file-icon {{
            font-size: 0.95rem;
            opacity: 0.8;
            width: 18px;
            text-align: center;
            flex-shrink: 0;
        }}

        .sec-icon {{
            color: var(--brand-sec);
        }}

        .horizon-icon {{
            color: var(--brand-horizon);
        }}

        .file-name {{
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            min-width: 0;
        }}

        .file-badge {{
            flex-shrink: 0;
            font-size: 0.7rem;
            padding: 0.15rem 0.45rem;
            border-radius: 10px;
            background: var(--pico-muted-border-color);
            color: var(--pico-muted-color);
            font-weight: 600;
            white-space: nowrap;
        }}

        .sec-badge {{
            background: rgba(225, 29, 72, 0.15);
            color: var(--brand-sec);
        }}

        .horizon-badge {{
            background: rgba(139, 92, 246, 0.15);
            color: var(--brand-horizon);
        }}

        /* Workspace Main Pane */
        .workspace {{
            min-width: 0;
            width: 100%;
        }}

        .view-panel {{
            display: none;
        }}

        .view-panel.active {{
            display: block;
        }}

        .panel-meta {{
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .security-banner {{
            border-left: 4px solid var(--brand-sec);
        }}

        .horizon-hero-card {{
            border-left: 4px solid var(--brand-horizon);
        }}

        .meta-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }}

        .meta-breadcrumbs {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.8rem;
            color: var(--pico-muted-color);
            margin-bottom: 0.4rem;
            font-family: var(--font-mono);
        }}

        .crumb-sep {{
            opacity: 0.5;
        }}

        .crumb.current {{
            color: var(--pico-color);
            font-weight: 600;
        }}

        .badge-pill {{
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            background: rgba(16, 185, 129, 0.12);
            color: var(--brand-primary);
            margin-left: 0.5rem;
        }}

        .badge-pill.sec-pill {{
            background: rgba(225, 29, 72, 0.12);
            color: var(--brand-sec);
        }}

        .badge-pill.horizon-pill {{
            background: rgba(139, 92, 246, 0.12);
            color: var(--brand-horizon);
        }}

        .meta-title {{
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
        }}

        .meta-actions {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
            flex-wrap: wrap;
        }}

        /* Document View Mode Toggle */
        .doc-view-toggle {{
            display: inline-flex;
            background: var(--pico-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 2px;
            gap: 2px;
        }}

        .btn-toggle {{
            background: transparent;
            border: none;
            border-radius: 6px;
            padding: 0.3rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--pico-muted-color);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .btn-toggle.active {{
            background: var(--brand-primary);
            color: #ffffff;
        }}

        .btn-action {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.75rem;
            font-size: 0.825rem;
            border-radius: var(--border-radius);
            text-decoration: none;
            cursor: pointer;
            font-weight: 600;
            border: 1px solid var(--pico-muted-border-color);
            background: transparent;
            color: var(--pico-color);
            transition: all 0.15s ease;
        }}

        .btn-copy {{
            background: var(--brand-primary);
            color: #ffffff;
            border-color: var(--brand-primary);
        }}

        .btn-copy:hover {{
            background: var(--brand-primary-hover);
            border-color: var(--brand-primary-hover);
        }}

        .btn-contribute {{
            background: var(--brand-horizon);
            color: #ffffff;
            border-color: var(--brand-horizon);
        }}

        .btn-contribute:hover {{
            background: #7c3aed;
        }}

        .btn-link:hover {{
            background: var(--pico-muted-border-color);
        }}

        .meta-desc {{
            color: var(--pico-muted-color);
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }}

        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 0.85rem;
            margin-bottom: 1rem;
        }}

        .meta-card {{
            background: var(--pico-background-color);
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            border: 1px solid var(--pico-muted-border-color);
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}

        .card-label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--pico-muted-color);
            letter-spacing: 0.05em;
        }}

        .card-value {{
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .cmd-code {{
            font-family: var(--font-mono);
            font-size: 0.78rem;
            word-break: break-all;
            background: transparent;
            padding: 0;
            color: var(--brand-primary);
        }}

        .anchors-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-top: 0.2rem;
        }}

        .anchor-pill {{
            background: rgba(225, 29, 72, 0.12);
            color: var(--brand-sec);
            border: 1px solid rgba(225, 29, 72, 0.3);
            border-radius: 4px;
            padding: 0.1rem 0.4rem;
            font-size: 0.725rem;
            font-family: var(--font-mono);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .anchor-pill:hover {{
            background: var(--brand-sec);
            color: #ffffff;
        }}

        .features-details {{
            border-top: 1px solid var(--pico-muted-border-color);
            padding-top: 0.75rem;
            margin-top: 0.75rem;
        }}

        .features-details summary {{
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--pico-color);
        }}

        .features-list {{
            margin: 0.65rem 0 0 0;
            padding-left: 1.5rem;
            font-size: 0.875rem;
            color: var(--pico-muted-color);
        }}

        .features-list li {{
            margin-bottom: 0.3rem;
        }}

        /* Security Table */
        .security-table-wrapper {{
            overflow-x: auto;
            margin-top: 1rem;
        }}

        .sec-matrix-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin: 0;
        }}

        .sec-matrix-table th {{
            background: var(--pico-background-color);
            padding: 0.6rem 0.8rem;
            text-align: left;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--pico-muted-color);
            border-bottom: 1px solid var(--pico-muted-border-color);
        }}

        .sec-matrix-table td {{
            padding: 0.65rem 0.8rem;
            border-bottom: 1px solid var(--pico-muted-border-color);
            vertical-align: top;
        }}

        .anchor-code {{
            font-family: var(--font-mono);
            font-weight: 700;
            color: var(--brand-sec);
            background: rgba(225, 29, 72, 0.1);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.8rem;
            white-space: nowrap;
        }}

        .cwe-tag {{
            color: var(--pico-muted-color);
            font-family: var(--font-mono);
            font-size: 0.75rem;
        }}

        /* Rendered Document View */
        .doc-rendered-container {{
            display: none;
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 2.25rem;
            overflow-x: auto;
        }}

        .doc-rendered-container.active {{
            display: block;
        }}

        .doc-article {{
            font-size: 0.95rem;
            line-height: 1.7;
        }}

        .doc-article h1, .doc-article h2, .doc-article h3, .doc-article h4 {{
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            font-weight: 700;
            border-bottom: 1px solid var(--pico-muted-border-color);
            padding-bottom: 0.35rem;
        }}

        .doc-article table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.875rem;
        }}

        .doc-article th, .doc-article td {{
            padding: 0.6rem 0.85rem;
            border: 1px solid var(--pico-muted-border-color);
        }}

        .doc-article th {{
            background: var(--pico-background-color);
            font-weight: 600;
        }}

        .doc-article pre {{
            background: var(--pico-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: 6px;
            padding: 1rem;
            overflow-x: auto;
            font-family: var(--font-mono);
            font-size: 0.85rem;
        }}

        .doc-article code {{
            font-family: var(--font-mono);
            font-size: 0.85rem;
            background: var(--pico-background-color);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
        }}

        .doc-article blockquote {{
            border-left: 4px solid var(--brand-primary);
            padding-left: 1rem;
            margin-left: 0;
            color: var(--pico-muted-color);
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

        .doc-raw-container {{
            display: none;
        }}

        .doc-raw-container.active {{
            display: block;
        }}

        .code-view {{
            max-height: 700px;
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
            padding: 0.65rem 0.5rem 0.65rem 0.75rem;
            text-align: right;
            border-right: 1px solid var(--pico-muted-border-color);
            color: var(--pico-muted-color);
            opacity: 0.6;
            vertical-align: top;
            width: 45px;
        }}

        .code-container td.code {{
            padding: 0.65rem 1rem;
            vertical-align: top;
        }}

        .code-container pre {{
            margin: 0;
            background: transparent;
            padding: 0;
            border: none;
            overflow: visible;
        }}

        /* Horizon Blueprint Grid */
        .horizon-blueprint-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.25rem;
            margin-top: 1rem;
            border-top: 1px solid var(--pico-muted-border-color);
            padding-top: 1rem;
        }}

        .blueprint-section h3 {{
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }}

        .blueprint-list {{
            padding-left: 1.25rem;
            margin: 0;
            font-size: 0.875rem;
            color: var(--pico-muted-color);
        }}

        .blueprint-list li {{
            margin-bottom: 0.25rem;
        }}

        .horizon-cta {{
            margin-top: 1.25rem;
            padding: 1.25rem;
            background: var(--pico-background-color);
            border-radius: var(--border-radius);
            border: 1px solid var(--pico-muted-border-color);
            text-align: center;
        }}

        .horizon-cta h3 {{
            margin: 0 0 0.4rem 0;
            font-size: 1.1rem;
        }}

        .horizon-cta p {{
            margin: 0;
            font-size: 0.875rem;
            color: var(--pico-muted-color);
        }}

        .text-link-btn {{
            background: transparent;
            border: none;
            color: var(--brand-primary);
            text-decoration: underline;
            cursor: pointer;
            padding: 0;
            font-size: inherit;
            font-family: inherit;
        }}

        /* Explanatory Sections */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin: 3.5rem 0 1.5rem 0;
        }}

        .info-card {{
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
        }}

        .info-card h3 {{
            margin-top: 0;
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .info-card p {{
            color: var(--pico-muted-color);
            font-size: 0.9rem;
            margin-bottom: 0;
        }}

        footer.site-footer {{
            border-top: 1px solid var(--pico-muted-border-color);
            padding: 2.5rem 2rem;
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

        @media (max-width: 960px) {{
            .explorer-layout {{
                grid-template-columns: 1fr;
                padding: 0 1rem 3rem 1rem;
            }}
            .explorer-sidebar {{
                position: static;
                max-height: none;
            }}
            .nav-container, .hero {{
                padding: 0 1rem;
            }}
            .hero h1 {{ font-size: 2rem; }}
            .meta-header {{ flex-direction: column; }}
            .meta-actions {{ width: 100%; }}
            .btn-action {{ flex: 1; justify-content: center; }}
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
                <a href="#explorer" class="nav-link">Code Explorer</a>
                <a href="#principles" class="nav-link">Principles</a>
                <a href="https://gitlab.com/renich/omni" target="_blank" rel="noopener" class="nav-link">GitLab</a>
                <a href="https://github.com/renich/omni" target="_blank" rel="noopener" class="nav-link">GitHub</a>
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
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 0 1-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 0 1 4.82 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0 1 18.6 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.51L23 13.45a.84.84 0 0 1-.35.94z"></path></svg>
                GitLab Upstream (Canonical)
            </a>
            <a href="https://github.com/renich/omni" target="_blank" rel="noopener" class="mirror-pill">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
                GitHub Mirror (SHA-1)
            </a>
            <a href="https://git.openlat.dev/renich/omni" target="_blank" rel="noopener" class="mirror-pill">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                OpenLat Mirror
            </a>
            <a href="https://liberapay.com/Renich/donate" target="_blank" rel="noopener" class="mirror-pill donate">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                Support on Liberapay
            </a>
        </div>
    </section>

    <main class="explorer-layout" id="explorer">
        <!-- Sidebar Explorer -->
        <aside class="explorer-sidebar">
            <div class="sidebar-section">
                <div class="section-header">
                    <span><span class="status-dot"></span>C (Verified Suite)</span>
                    <span>5 Editions</span>
                </div>
                <div class="nav-tree">
                    {c_tree_str}
                </div>
            </div>

            <div class="sidebar-section">
                <div class="section-header">
                    <span><span class="status-dot horizon"></span>Target Horizons</span>
                    <span>7 Planned</span>
                </div>
                <div class="nav-tree">
                    {horizon_tree_str}
                </div>
            </div>

            <div class="sidebar-section">
                <div class="section-header">
                    <span>Repository Docs</span>
                    <span>Guidelines</span>
                </div>
                <div class="nav-tree">
                    {docs_tree_str}
                </div>
            </div>
        </aside>

        <!-- Main Workspace -->
        <section class="workspace">
            {panels_str}

            <section class="info-grid" id="principles">
                <div class="info-card">
                    <h3>The Scalar State Accumulator</h3>
                    <p>
                        Rather than polluting code with dead <code>(void)var;</code> suppression casts, Omni mathematically consumes every declared scalar into a single state hash. This forces the optimizer and semantic analyzer to evaluate all symbols while compiling cleanly under <code>-Wall -Wextra -Werror</code>.
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
        </section>
    </main>

    <footer class="site-footer">
        <p>
            Omni &mdash; Maintained by <a href="https://evalinux.com" target="_blank" rel="noopener">R&eacute;nich Bon &Cacute;iri&cacute;</a> and contributors.
        </p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            Licensed under the <a href="https://gitlab.com/renich/omni/-/blob/master/LICENSE" target="_blank" rel="noopener">GNU General Public License v3.0 or later</a>. Canonical upstream on <a href="https://gitlab.com/renich/omni" target="_blank" rel="noopener">GitLab</a>, mirrored on <a href="https://github.com/renich/omni" target="_blank" rel="noopener">GitHub</a> and <a href="https://git.openlat.dev/renich/omni" target="_blank" rel="noopener">OpenLat</a>.
        </p>
    </footer>

    <script>
        function switchView(viewId) {{
            document.querySelectorAll('.nav-tree-item').forEach(btn => {{
                btn.classList.remove('active');
            }});
            document.querySelectorAll('.view-panel').forEach(panel => {{
                panel.classList.remove('active');
            }});

            const targetBtn = document.getElementById('btn-' + viewId);
            const targetPanel = document.getElementById('panel-' + viewId);

            if (targetBtn && targetPanel) {{
                targetBtn.classList.add('active');
                targetPanel.classList.add('active');
                if (history.replaceState) {{
                    history.replaceState(null, null, '#' + viewId);
                }} else {{
                    window.location.hash = viewId;
                }}
            }}
        }}

        function setDocMode(docId, mode) {{
            const renderedBox = document.getElementById('doc-rendered-' + docId);
            const rawBox = document.getElementById('doc-raw-' + docId);
            const btnDoc = document.getElementById('btn-mode-doc-' + docId);
            const btnRaw = document.getElementById('btn-mode-raw-' + docId);

            if (mode === 'doc') {{
                if (renderedBox) renderedBox.classList.add('active');
                if (rawBox) rawBox.classList.remove('active');
                if (btnDoc) btnDoc.classList.add('active');
                if (btnRaw) btnRaw.classList.remove('active');
            }} else {{
                if (renderedBox) renderedBox.classList.remove('active');
                if (rawBox) rawBox.classList.add('active');
                if (btnDoc) btnDoc.classList.remove('active');
                if (btnRaw) btnRaw.classList.add('active');
            }}
        }}

        function copyContent(viewId) {{
            const rawTextArea = document.getElementById('raw-' + viewId);
            const copyBtnText = document.getElementById('copy-text-' + viewId);
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

        // Initialize saved theme or system preference and route to initial view
        (function() {{
            const savedTheme = localStorage.getItem('omni-theme');
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
            document.documentElement.setAttribute('data-theme', initialTheme);
            updateThemeUI(initialTheme);

            const hash = window.location.hash ? window.location.hash.substring(1) : 'c-c23';
            if (document.getElementById('panel-' + hash)) {{
                switchView(hash);
            }} else {{
                switchView('c-c23');
            }}
        }})();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / "public"
    build_site(repo_root, output_dir)
