=============================
Repository Architecture Guide
=============================

Structural design, directory layout, and build harness conventions for omni.

Design Philosophy
=================

Omni is structured as a polyglot language compendium. Each programming language occupies its own isolated subdirectory, maintaining self-contained documentation, security guidelines, and source reference files.

A single root ``GNUmakefile`` coordinates detection, compilation, and test execution across all supported toolchains without polluting language directories.

Directory Hierarchy
===================

.. code-block:: text

   omni/
   ├── GNUmakefile
   ├── README.rst
   ├── CONTRIBUTING.rst
   ├── CHANGELOG.rst
   ├── docs/
   │   ├── architecture.rst
   │   └── process.rst
   └── <language>/
       ├── README.rst
       ├── security.rst
       └── <standard>.<ext>

Subdirectory Responsibilities
=============================

Language Root Directory
-----------------------

Each language directory is named using the lowercase canonical name of the language (for example, ``c/``, ``cpp/``, ``zig/``, ``crystal/``, ``go/``, ``rust/``, ``python/``).

Reference Source Files
----------------------

* Source filenames represent the formal standard edition or language revision (for example, ``c89.c``, ``c99.c``, ``c11.c``, ``c17.c``, ``c23.c``, or ``cpp20.cpp``, ``cpp23.cpp``).
* If a language does not have formal versioned ISO standards, use major/minor releases (for example, ``py312.py`` or ``zig014.zig``).
* Each source file must be completely self-contained and buildable with standard toolchains.

Language README: README.rst
---------------------------

Every language directory contains a ``README.rst`` defining:

* The standards matrix and formal document identifiers.
* Distinguishing language features added or removed in each revision.
* Compiler baseline and mandatory compilation flags.
* Verification commands specific to that language.

Security Catalog: security.rst
------------------------------

Every language that permits memory manipulation, non-local control flow, or unchecked concurrency must provide a ``security.rst`` threat model matrix linking inline source code tags (``[!SECURITY-NOTE: ID]``) to formal vulnerability analyses and production remediation guidelines.

Build System Invariants
=======================

The root ``GNUmakefile`` enforces the following requirements across all languages:

1. **Parse-Time Toolchain Inspection**: All compiler detection uses Make parse-time evaluation (``command -v <tool>``). Shell conditional blocks inside recipes must never be used to skip compilation, as missing output binaries break Make target idempotency.
2. **Dynamic Target Generation**: Target lists are constructed programmatically using ``foreach`` expansions across available toolchains and language standards.
3. **Automatic Error Cleanup**: ``.DELETE_ON_ERROR:`` is enabled globally to ensure interrupted builds delete partial target artifacts.
4. **Strict Shell Defaults**: ``SHELL`` is set to ``/usr/bin/bash`` with ``.SHELLFLAGS := -euo pipefail -c`` to guarantee immediate pipeline failure detection.
5. **Standardized Check Targets**: The build harness exposes uniform top-level targets:
   * ``make all``: Default target, runs ``make check``.
   * ``make check``: Builds and executes all verified language implementations across all detected compilers.
   * ``make check-<language>``: Verifies all editions for a specific language (for example, ``make check-c``).
   * ``make check-<standard>``: Verifies a single edition (for example, ``make check-c23``).
   * ``make clean``: Cleans the ``build/`` artifact directory.
