====================================
Language Compendium Creation Process
====================================

Architectural methodology for authoring, validating, and maintaining omni language reference files.

Overview
========

Creating an omni file is an exercise in dense, exhaustive language synthesis. Unlike conventional tutorials or code samples, an omni compendium captures 100% of a language's normative grammar, keywords, types, attributes, and preprocessor facilities within the smallest possible single, self-contained, executable file.

This document formalizes the 6-phase engineering lifecycle required for any language added to the repository.

Phase 1: Normative Standard Extraction
======================================

Every omni implementation must be anchored to an authoritative specification; never rely on colloquial documentation or associative memory.

Research Checklist
------------------

* **Lexical Keyword Table**: Extract the complete list of reserved words, contextual keywords, and retained backward-compatibility tokens from the formal standard grammar.
* **Type System Catalog**: Identify all primitive scalar types, exact-width integers, floating-point formats, pointers, references, composites, and user-defined type declarators.
* **Operators and Precedence**: Catalogue every unary, binary, ternary, assignment, and compound operator across all precedence tiers.
* **Literal Grammars**: Identify every valid literal form: octal, hexadecimal, binary, digit separators, character sets, wide characters, unicode encodings, and raw strings.
* **Preprocessor and Attributes**: List all directives, macro operators, conditional inclusion mechanisms, and standardized attributes.

Phase 2: Single-File Architecture
=================================

An omni reference file must remain strictly self-contained. External user-defined headers are prohibited; only standard library interfaces defined by the language specification are permitted.

Structure the implementation into four sequential logical sections:

* **Section 1: Directives and Metaprogramming**: Language version assertions, standard library imports, macro definitions, token concatenation, and stringification operators.
* **Section 2: Types, Declarators, and Interfaces**: Structs, unions, enums, typedefs, bitfields, function pointer signatures, qualified parameters, and generic interfaces.
* **Section 3: Optional Language Facilities**: Dual-path fallbacks for optional standard annexes or compiler-dependent capabilities.
* **Section 4: Execution Driver and State Accumulator**: The entrypoint function exercising control flow, literal forms, expressions, jumps, signal handlers, and scalar variable consumption.

Phase 3: Dual-Path Saturation Pattern
=====================================

Language standards frequently include optional annexes or conditionally supported features (for instance, ISO C Annex G Imaginary types, or Decimal Floating Point in Annex F). Compilers often omit support for these extensions while maintaining general conformance.

To achieve 100% lexical saturation without causing compilation errors on conformant compilers, apply the dual-path pattern:

.. code-block:: c

   #ifdef __STDC_IEC_60559_DFP__
   static _Decimal32  active_d32  = 1.0DF;
   static _Decimal64  active_d64  = 1.0DD;
   static _Decimal128 active_d128 = 1.0DL;
   #else
   #  if 0
   typedef _Decimal32  d32_ref;
   typedef _Decimal64  d64_ref;
   typedef _Decimal128 d128_ref;
   #  endif
   #endif

When the macro is defined by a supporting toolchain, the tokens participate in runtime execution. When unsupported, the tokens remain lexically present inside an inactive preprocessor branch, fulfilling the lexical saturation requirement while compiling cleanly under ``-Werror``.

Phase 4: Scalar State Accumulator Pattern
=========================================

Exercising every type, qualifier, and storage class creates dozens of variables. In production-grade compiler configurations with ``-Wall -Wextra -Werror``, unread variables trigger build-breaking ``unused-variable`` errors.

Suppressing these warnings with repeated cast expressions (such as ``(void)var;``) clutters the file and inflates line count with non-functional boilerplate.

Instead, consume every declared scalar variable in a single mathematical accumulator expression:

.. code-block:: c

   int validate_system_state(int legacy_auto, int fast_counter, double reg_double, char c_ascii) {
       double checksum = (double)legacy_auto + fast_counter + reg_double + c_ascii;
       if (checksum < 0.0) {
           return 1;
       }
       return 0;
   }

This technique provides three distinct advantages:

* Eliminates hundreds of lines of dead cast boilerplate.
* Mathematically forces the compiler's semantic analyzer and optimizer to evaluate all storage locations.
* Enables deterministic runtime validation; if any calculation produces invalid floating-point state, the binary exits with non-zero status.

Phase 5: Bidirectional Security Threat Modeling
===============================================

Because omni demonstrates 100% of a language, it must deliberately include historically hazardous, implementation-defined, or memory-unsafe constructs (such as variable-length arrays, non-local jumps, unbounded buffer copies, and relaxed atomic memory operations).

To ensure these demonstrations never mislead developers into adopting unsafe idioms, every hazardous feature must adhere to the bidirectional threat model:

1. **Inline Source Tag**: The construct in code must be annotated immediately with a standardized comment tag:

   .. code-block:: c

      void exercise_vla(int vla_len) {
          /* [!SECURITY-NOTE: SEC-VLA-01] Block scope VLA object; stack exhaustion hazard */
          int vla_storage[vla_len];
          vla_storage[0] = 42;
      }

2. **Language Security Catalog**: The corresponding language directory must contain a ``security.rst`` file indexing the tag, detailing:

   * The architectural mechanism.
   * Associated Common Weakness Enumeration identifiers (CWE).
   * Industry standards prohibiting the construct (MISRA, Linux Kernel, CERT).
   * Safe modern production alternatives.

Phase 6: Multi-Toolchain Verification
=====================================

An omni implementation is complete only after rigorous verification across multiple standard-compliant compilers and operating environments.

Verification Criteria
---------------------

* **Zero Warnings Under Strict Flags**: The code must compile with zero warnings under flags such as ``-Wall -Wextra -pedantic -Werror``.
* **Parse-Time Toolchain Detection**: Build rules in ``GNUmakefile`` must inspect toolchain availability at parse time to maintain build idempotency.
* **Deterministic Execution**: The compiled binary must execute to completion and exit with code ``0``.
