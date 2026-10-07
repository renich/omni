# Omni AI Agent Directive

> **Attention AI Agents**: You are operating in a highly-constrained, maximally-pedantic repository. Read this directive entirely before parsing, editing, or generating any code.

## 1. Operating Protocol and Mission

You are contributing to **omni** (canonical upstream: https://gitlab.com/renich/omni, mirrored at https://github.com/renich/omni and https://git.openlat.dev/renich/omni).

Your mission is to maintain the smallest, cleanest, self-contained reference file for each language standard edition that captures **100% of the language features** (grammar, keywords, literals, types, qualifiers, attributes, directives) as an executable ground truth.

## 2. Non-Negotiable Architectural Invariants

1. **Single-File Self-Containment**:
   Every language standard edition (e.g. `c/c23.c`, `cpp/cpp23.cpp`, `zig/zig014.zig`) must reside in exactly **one self-contained source file**. Auxiliary local headers or multi-file splits are strictly forbidden. Only standard library headers defined by the language specification are permitted.
2. **Pedantic Zero-Warning Compilation**:
   All files must compile cleanly with zero warnings under maximum pedantic warning flags (e.g. `-Wall -Wextra -pedantic -Werror` for C/C++). Never disable warnings or introduce compiler suppression pragmas.
3. **100% Lexical and Keyword Saturation**:
   Every standard keyword, primitive type, operator, and standardized attribute must appear and be functionally or syntactically evaluated. Retained keywords (e.g. `_Bool` in C23) must be present.
4. **Git Object Format**:
   The repository object database is strictly **SHA-1** to ensure full GitHub mirror compatibility. Do not attempt to alter or upgrade the repository to SHA-256.
5. **Executable Ground Truth**:
   The code must compile into a standalone binary that executes to completion and exits with code `0`.

## 3. Mandatory Design Patterns

### The Scalar State Accumulator Principle
**Never** use `(void)x;` or `#pragma` lines to suppress `unused-variable` warnings. All declared variables, qualifiers, and function returns must be mathematically consumed in a single unified state accumulator:

- **Prohibited**:
  ```c
  int val = 42;
  (void)val; /* Dead suppression line */
  ```
- **Mandatory**:
  ```c
  double checksum = (double)legacy_auto + fast_counter + val + s_char;
  if (checksum < 0.0) {
      return 1;
  }
  ```

### Dual-Path Saturation Pattern
For optional language annexes or conditionally supported extensions (e.g. Annex G `_Imaginary` or Decimal Floating Point):
- If the feature macro is defined, exercise it at runtime.
- If unsupported by the compiler, keep declarations inside an `#else` (or `#if 0`) block so the tokens remain physically present for lexical saturation scanners without breaking compilation.

### Bidirectional Security Anchors
Whenever code demonstrates historically hazardous, implementation-defined, or memory-unsafe features:
1. Annotate inline with: `[!SECURITY-NOTE: SEC-<ID>]`.
2. Ensure the ID is cataloged in the language directory's `security.rst` with architectural analysis, CWE mapping, and safe production alternatives.

## 4. Anti-Hallucination Guardrails

- **Standard Conformance Only**: Do not use non-standard vendor extensions (e.g. GNU `__attribute__`, `__builtin_*`) unless explicitly standardized in the edition being showcased.
- **Inspect Before Asserting**: The `GNUmakefile` uses parse-time toolchain detection (`command -v`). Never guess compiler capabilities; inspect the Makefile and verify on disk.
- **Format Preservation**: Human-facing documentation (`README.rst`, `docs/*.rst`, `c/*.rst`) is strictly ReStructuredText (`.rst`), validated via `rstcheck`. Agent rule files (`AGENTS.md`, `.agents/rules/*.md`) are the only Markdown files permitted.

## 5. Verification Checkpoint

Before presenting any solution or finalizing edits, verify:
1. Did you consume all new variables in the scalar state accumulator?
2. Does `make clean && make check` pass cleanly across all detected compilers?
3. Does `make check-docs` report zero errors and zero warnings?
4. Did you preserve single-file self-containment?
