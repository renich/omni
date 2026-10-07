============================
C23 Reference Implementation
============================

The canonical, minimal ISO/IEC 9899:2024 (C23) reference implementation for omni.

Executive Summary
=================

``c/c23.c`` is a single-file, exhaustive compendium of the modern C language under the ISO/IEC 9899:2024 standard. It demonstrates all grammar additions, keywords, type specifiers, preprocessor features, and standard attributes introduced or updated in C23 while compiling cleanly under strict zero-warning compiler configurations.

Toolchain Baseline
==================

The reference file is tested against the following toolchain baseline:

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Compiler
     - Tested Version
     - Invocation

   * - GCC
     - 16.2+
     - ``gcc -std=c23 -Wall -Wextra -pedantic -Werror -pthread c23.c -lm -o c23``

   * - LLVM Clang
     - 22.1+
     - ``clang -std=c23 -Wall -Wextra -pedantic -Werror -pthread c23.c -lm -o c23``

Specification Coverage Matrix
=============================

.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - ISO C23 Clause
     - Focus Area
     - Key Features Exercised

   * - Clause 6.4
     - Lexical elements
     - Binary literals ``0b...``, digit separators ``'``, UTF-8 char ``u8'...'``, standard keywords (``bool``, ``true``, ``false``, ``nullptr``, ``alignas``, ``alignof``, ``constexpr``, ``thread_local``, ``typeof``, ``typeof_unqual``).

   * - Clause 6.5
     - Expressions and operators
     - ``_Generic`` selection, precedence chaining, compound assignments, bitwise logic, ternary expressions, comma operator.

   * - Clause 6.7
     - Declarations and types
     - ``_BitInt(N)`` with ``wb``/``uwb`` suffixes, fixed underlying enum types (``enum Tag : uint8_t``), anonymous structs and unions, flexible array members, universal zero-initialization ``{}``, designated initializers, compound literals.

   * - Clause 6.7.12
     - Standard attributes
     - ``[[nodiscard]]`` with optional reason string, ``[[deprecated]]``, ``[[fallthrough]]``, ``[[maybe_unused]]``, ``[[noreturn]]``, ``[[reproducible]]``, ``[[unsequenced]]``.

   * - Clause 6.8
     - Statements and control flow
     - Labels preceding declarations, labels terminating compound statements without null statements, loops, jump statements.

   * - Clause 6.9
     - Function declarations
     - Modern empty parameter list semantics (``f()`` identical to ``f(void)``), variable-length array prototype notation ``[*]``, array parameter qualifiers (``static restrict``).

   * - Clause 6.10
     - Preprocessor directives
     - Direct binary inclusion with ``#embed`` (featuring ``limit``, ``prefix``, ``suffix``, ``if_empty``), ``__VA_OPT__`` variadic expansions, ``#elifdef``, ``#elifndef``, ``__has_embed``, ``__has_include``, ``__has_c_attribute``, ``#warning``, ``_Pragma``.

Compilation and Execution
=========================

Build the executable:

.. code-block:: bash

   gcc -std=c23 -Wall -Wextra -pedantic -Werror -pthread c23.c -lm -o c23

Run the verification harness:

.. code-block:: bash

   ./c23
