=========
Changelog
=========

All notable changes to the omni project are documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_, and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
==========

.. rubric:: Added

* Community call for contributions across upcoming programming languages: C++, Zig, Crystal, Go, Rust, and Python.
* Contributor guidelines in ``CONTRIBUTING.rst`` and comprehensive methodology guides in ``docs/process.rst`` and ``docs/architecture.rst``.

0.1.0 - 2026-10-07
==================

.. rubric:: Added

* Canonical C language compendium suite covering all ratified ISO C standard editions:

  * ANSI X3.159-1989 / ISO/IEC 9899:1990 (``c/c89.c``).
  * ISO/IEC 9899:1999 (``c/c99.c``).
  * ISO/IEC 9899:2011 (``c/c11.c``).
  * ISO/IEC 9899:2018 (``c/c17.c``).
  * ISO/IEC 9899:2024 (``c/c23.c``).

* Exhaustive keyword saturation: 59/59 keywords in C23, full primitive keyword coverage (including ``_Bool`` and dual-path ``_Imaginary``) across C99, C11, and C17.
* Dual-Path Saturation Pattern for conditionally supported ISO Annexes (Annex G Imaginary types and Annex F/H Decimal Floating Point).
* Mathematical scalar state accumulator (checksum) consuming all declared variables without dead cast suppression lines.
* Threat model catalog in ``c/security.rst`` with bidirectional source code anchor annotations (``SEC-VLA-01``, ``SEC-JMP-01``, ``SEC-BITFIELD-01``, ``SEC-ATOMIC-01``, ``SEC-C89-UNBOUNDED-01``).
* Dynamic root ``GNUmakefile`` featuring parse-time toolchain detection for GCC and Clang, automatic ``.DELETE_ON_ERROR`` cleanup, and strict bash pipefail execution flags.
* Standards documentation and compiler requirements in ``c/README.rst``.
