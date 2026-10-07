====
omni
====

The smallest piece of code that showcases the entirety of a programming language.

Executive Summary
=================

Omni provides a single, canonical, self-contained reference file per language that exercises 100% of its grammar, syntax, type system, attributes, preprocessor facilities, and literal forms. Each language implementation compiles cleanly under strict, zero-warning flags and acts as an executable Rosetta stone for human engineers and automated systems.

Core Design Tenets
==================

* **Complete Language Saturation**: Every standard keyword, operator, type qualifier, literal format, attribute, and preprocessor directive is exercised.
* **Minimal Footprint**: Maximum semantic density without gratuitous boilerplate or dead suppression code.
* **Executable Ground Truth**: Every file must compile cleanly under modern standard-compliant compilers with pedantic warnings enabled.
* **Zero Cognitive Padding**: Code is structured as an immediate, searchable syntax reference rather than an introductory tutorial.

Supported Languages
===================

.. list-table::
   :widths: 20 25 35 20
   :header-rows: 1

   * - Language
     - Standard
     - Reference File
     - Status

   * - C
     - ISO/IEC 9899:2024, C23
     - ``c/c23.c``
     - Verified

Repository Structure
====================

.. code-block:: text

   omni/
   ├── GNUmakefile
   ├── README.rst
   └── c/
       ├── README.rst
       └── c23.c

Verification
============

Build and verify all language implementations using GNU Make:

.. code-block:: bash

   make check

To verify an individual language target:

.. code-block:: bash

   make check-c
