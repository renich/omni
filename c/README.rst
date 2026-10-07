============================
C Reference Implementations
============================

Canonical, minimal C reference implementations across all standard iterations from C89 to C23.

Executive Summary
=================

The ``c/`` directory provides an exhaustive, self-contained syntax compendium for each ratified edition of the ISO/IEC 9899 standard. Each file exercises 100% of the language features introduced or permitted by its respective standard while strictly omitting constructs from future editions. All implementations compile cleanly under both GCC and Clang with maximum warning enforcement and zero warnings permitted.

Standards Matrix
================

.. list-table::
   :widths: 15 25 25 35
   :header-rows: 1

   * - Standard
     - Formal Identifier
     - File
     - Distinguishing Additions

   * - C89/C90
     - ANSI X3.159-1989, ISO/IEC 9899:1990
     - ``c/c89.c``
     - Declarations strictly before statements, K&R compatibility, no trailing commas in enums, exact 32 keywords.

   * - C99
     - ISO/IEC 9899:1999
     - ``c/c99.c``
     - Mixed declarations, line comments, ``for`` loop declarations, ``long long``, ``_Bool``, ``inline``, ``restrict``, VLAs, flexible array members, designated initializers, compound literals, variadic macros, ``__func__``, hex floats.

   * - C11
     - ISO/IEC 9899:2011
     - ``c/c11.c``
     - ``_Static_assert``, ``_Alignas``, ``_Alignof``, ``_Atomic``, ``_Generic``, ``_Noreturn``, ``_Thread_local``, anonymous structs and unions, ``char16_t`` and ``char32_t`` unicode literals.

   * - C17
     - ISO/IEC 9899:2018
     - ``c/c17.c``
     - Defect-report resolution release; ``__STDC_VERSION__ = 201710L``; deprecation of ``ATOMIC_VAR_INIT``.

   * - C23
     - ISO/IEC 9899:2024
     - ``c/c23.c``
     - Extended ``#embed``, standard attributes (``[[nodiscard]]``, ``[[reproducible]]``, etc.), ``constexpr``, ``nullptr``, ``auto`` type deduction, ``typeof``, ``typeof_unqual``, ``_BitInt``, binary literals, digit separators, UTF-8 char constants, labels anywhere.

Toolchain Baseline
==================

All implementations are continuously verified against the following toolchains:

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Target
     - Standard Flag
     - Enforced Compiler Flags

   * - C89
     - ``-std=c89``
     - ``-Wall -Wextra -pedantic -Werror -lm``

   * - C99
     - ``-std=c99``
     - ``-Wall -Wextra -pedantic -Werror -lm``

   * - C11
     - ``-std=c11``
     - ``-Wall -Wextra -pedantic -Werror -pthread -lm``

   * - C17
     - ``-std=c17``
     - ``-Wall -Wextra -pedantic -Werror -pthread -lm``

   * - C23
     - ``-std=c23``
     - ``-Wall -Wextra -pedantic -Werror -pthread -lm``

Verification and Execution
==========================

To build and execute all C standard implementations:

.. code-block:: bash

   make check-c

To verify an individual standard:

.. code-block:: bash

   make check-c89
   make check-c99
   make check-c11
   make check-c17
   make check-c23
