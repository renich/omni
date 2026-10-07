====
omni
====

The smallest piece of code that showcases the entirety of a programming language.

Overview
========

Omni provides a single, canonical, self-contained reference file per language that exercises 100% of its grammar, syntax, type system, attributes, preprocessor facilities, and literal forms.

Each implementation compiles cleanly under strict, zero-warning flags and acts as an executable Rosetta stone for human engineers, compiler authors, and AI coding agents.

Core Principles
===============

* **Complete Language Saturation**: Every standard keyword, operator, type qualifier, literal format, attribute, and preprocessor directive is exercised.
* **Minimal Footprint**: Maximum semantic density without gratuitous boilerplate or dead suppression code.
* **Executable Ground Truth**: Every file compiles cleanly with pedantic warnings enabled and exits with status code ``0``.
* **Bidirectional Threat Modeling**: Hazardous or historical constructs are linked inline to formal security hazard entries in an accompanying threat catalog.
* **Zero Cognitive Padding**: Code is structured as an immediate, searchable syntax reference rather than an introductory tutorial.

Supported Languages and Standards
=================================

.. list-table::
   :widths: 15 35 30 20
   :header-rows: 1

   * - Language
     - Standard
     - Reference File
     - Status

   * - C
     - ANSI X3.159-1989, ISO/IEC 9899:1990
     - ``c/c89.c``
     - Verified

   * - C
     - ISO/IEC 9899:1999
     - ``c/c99.c``
     - Verified

   * - C
     - ISO/IEC 9899:2011
     - ``c/c11.c``
     - Verified

   * - C
     - ISO/IEC 9899:2018
     - ``c/c17.c``
     - Verified

   * - C
     - ISO/IEC 9899:2024
     - ``c/c23.c``
     - Verified

Language Horizon and Contributions
==================================

Omni is expanding across modern and systems programming languages. We actively invite reference implementations for the following targets:

* **C++**: ISO/IEC 14882 editions (C++98 through C++23 and C++26).
* **Zig**: Versions 0.13, 0.14, and development tracks.
* **Crystal**: Version 1.12 through current releases.
* **Go**: Modern Go editions with generics and context propagation.
* **Rust**: 2015, 2018, 2021, and 2024 editions.
* **Python**: Python 3.8 through 3.13.
* **Bash**: POSIX and GNU Bash 5.x standards.

If you wish to contribute a language or standard, review the :doc:`CONTRIBUTING` guide and our architectural methodology in :doc:`docs/process`.

Quickstart and Verification
===========================

Build and verify all language implementations using GNU Make:

.. code-block:: bash

   make check

To verify all standards for a specific language:

.. code-block:: bash

   make check-c

To verify an individual standard edition:

.. code-block:: bash

   make check-c89
   make check-c99
   make check-c11
   make check-c17
   make check-c23

Documentation Index
===================

* :doc:`CONTRIBUTING`: Contribution requirements, workflow, and submission checklist.
* :doc:`docs/process`: Detailed 6-phase engineering lifecycle for authoring compendiums.
* :doc:`docs/architecture`: Repository layout, naming conventions, and build system invariants.
* :doc:`c/README`: C language standards matrix, compiler baselines, and execution notes.
* :doc:`c/security`: Threat model catalog and security advisories for hazardous C features.
* :doc:`CHANGELOG`: Project version history and changelog.
