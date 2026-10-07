==============================
Language Standards and Roadmap
==============================

Complete inventory of supported language specifications, reference implementations, and active target horizons.

Overview
========

Omni provides a single, canonical, self-contained reference file for each language standard edition that captures 100% of its grammar, syntax, type system, attributes, preprocessor facilities, and literal forms.

This document details all verified language editions, toolchain compilation baselines, and upcoming target standards.

Current Supported Standards
===========================

The following reference implementations are fully implemented, verified with zero compiler warnings under pedantic enforcement, and tested to exit with status code ``0``:

.. list-table::
   :widths: 12 18 32 18 20
   :header-rows: 1

   * - Language
     - Standard
     - Formal Specification
     - Reference File
     - Verification Status

   * - C
     - C89/C90
     - ANSI X3.159-1989, ISO/IEC 9899:1990
     - ``c/c89.c``
     - Verified (GCC, Clang)

   * - C
     - C99
     - ISO/IEC 9899:1999
     - ``c/c99.c``
     - Verified (GCC, Clang)

   * - C
     - C11
     - ISO/IEC 9899:2011
     - ``c/c11.c``
     - Verified (GCC, Clang)

   * - C
     - C17
     - ISO/IEC 9899:2018
     - ``c/c17.c``
     - Verified (GCC, Clang)

   * - C
     - C23
     - ISO/IEC 9899:2024
     - ``c/c23.c``
     - Verified (GCC, Clang)

For distinguishing features, compiler flags, and threat modeling for the C family, consult the `C Reference Suite <../c/README.rst>`_ and the `C Security Threat Model <../c/security.rst>`_ catalog.

Language Horizon and Roadmap
============================

Omni is systematically expanding across systems and modern programming languages. Contributions are actively solicited for the following targets:

C++ Family
----------

ISO/IEC 14882 standard revisions represent major syntactic expansions across decades:

* **C++98/C++03** (``cpp/cpp98.cpp``): Templates, exceptions, namespaces, runtime type information, standard library streams.
* **C++11** (``cpp/cpp11.cpp``): Move semantics, rvalue references, lambda expressions, ``auto`` type deduction, ``constexpr``, smart pointers, memory model.
* **C++14** (``cpp/cpp14.cpp``): Generic lambdas, relaxed ``constexpr``, binary literals, variable templates.
* **C++17** (``cpp/cpp17.cpp``): Structured bindings, ``if constexpr``, fold expressions, class template argument deduction, filesystem, ``std::string_view``.
* **C++20** (``cpp/cpp20.cpp``): Concepts and constraints, coroutines, modules, three-way comparison operator, ranges.
* **C++23** (``cpp/cpp23.cpp``): Explicit object parameter (deducing this), multidimensional subscript, standard library modules, expected.

Zig Family
----------

Zig targets explicit memory control, comptime execution, and absence of hidden control flow:

* **Zig 0.13.0** (``zig/zig013.zig``): Established comptime reification, explicit allocators, tagged unions, error handling.
* **Zig 0.14.0** (``zig/zig014.zig``): Updated standard library layouts, modified comptime reflection builtins, IO abstractions.

Crystal Family
--------------

Crystal blends expressive syntax with compiled type safety, fiber concurrency, and macro metaprogramming:

* **Crystal 1.x** (``crystal/crystal1.cr``): Type unions, fibers, channels, execution contexts, macro expansion, C ABI bindings, nil-safety.

Go Family
---------

Go prioritizes communicative concurrency, interface abstraction, and structural simplicity:

* **Modern Go** (``go/go122.go``): Goroutines, channels, interfaces, type parameters (generics), loop variable semantics, context propagation.

Rust Family
-----------

Rust editions define epochal evolution of compiler semantics and borrow checking:

* **Rust 2018** (``rust/rust2018.rs``): Non-lexical lifetimes, path clarity, trait object syntax.
* **Rust 2021** (``rust/rust2021.rs``): Disjoint capture in closures, IntoIterator for arrays, panic macro changes.
* **Rust 2024** (``rust/rust2024.rs``): Return position impl Trait in traits, async closures, revised unsafe attributes.

Python Family
-------------

Python provides rich structural grammar and expressive typing within interpreted environments:

* **Python 3.10-3.13** (``python/py313.py``): Structural pattern matching (``match``/``case``), union type operators (``|``), exception groups, type parameter syntax (PEP 695).

Bash and POSIX Shell Family
---------------------------

Shell scripting standards govern systems orchestration and POSIX compatibility:

* **GNU Bash 5.x** (``bash/bash5.bash``): Associative arrays, parameter transformation, arithmetic evaluation, coprocesses, process substitution.
* **POSIX.1-2024 Shell** (``sh/sh2024.sh``): Pure POSIX command language without non-standard extensions.

Contributing a Language Target
==============================

To introduce a new language or standard edition to omni:

1. Follow the 6-phase engineering lifecycle in `process.rst <process.rst>`_.
2. Adhere to repository layout conventions in `architecture.rst <architecture.rst>`_.
3. Verify requirements and testing checklists in `CONTRIBUTING.rst <../CONTRIBUTING.rst>`_.
