=======================
Contributing Guidelines
=======================

Guidelines for authoring and submitting language reference implementations to omni.

Philosophy and Scope
====================

Omni aims to provide the single smallest, cleanest, self-contained reference file for every major programming language and language standard edition. Each file serves as an executable Rosetta stone, capturing 100% of the grammar, keywords, types, attributes, and directives of the target language.

We welcome contributions of new languages, newer or historical standard editions, and verification improvements.

Core Requirements for Contributions
===================================

Every language implementation submitted to omni must satisfy six non-negotiable criteria:

1. **Single Self-Contained Source File**: All syntax must reside in a single source file without auxiliary user headers or multi-file dependencies.
2. **Exhaustive Lexical and Grammar Saturation**: Every normative keyword, operator, literal representation, type qualifier, and standardized attribute must appear and be functionally or syntactically exercised.
3. **Minimal Footprint**: Maximize density and eliminate dead code. Avoid dozens of individual suppression casts; use a single mathematical accumulator or scalar state consumer.
4. **Dual-Path Saturation Pattern**: For optional annexes or compiler-dependent extensions, use conditional compilation with an `#if 0` or inactive block fallback so the tokens are lexically present without failing builds on standard-compliant compilers.
5. **Zero-Warning Pedantic Compilation**: The code must compile cleanly under maximum warning enforcement flags (for example, ``-Wall -Wextra -pedantic -Werror`` for C/C++).
6. **Executable Ground Truth**: The code must compile to an executable binary that completes successfully and exits with status code ``0``.

Step-by-Step Submission Process
===============================

Step 1: Consult the Creation Process Guide
------------------------------------------

Before writing code, read `Compendium Creation Process <docs/process.rst>`_ to understand the standard extraction methodology, state accumulator design, and dual-path fallback patterns.

Step 2: Create the Language Directory
-------------------------------------

Create a new directory named after the lowercase canonical language identifier (for example, ``cpp/``, ``zig/``, ``crystal/``, ``go/``, ``rust/``, ``python/``).

Populate the directory with three essential files:

* ``<language>/<standard>.<ext>``: The canonical reference implementation (for example, ``cpp23.cpp``, ``zig014.zig``).
* ``<language>/README.rst``: The language-specific matrix, compiler requirements, and test targets.
* ``<language>/security.rst``: Threat model and hazard catalog for any memory-unsafe or non-local language constructs demonstrated.

Step 3: Integrate with GNUmakefile
----------------------------------

Add your language targets into the root ``GNUmakefile`` adhering to build invariants:

* Inspect toolchain availability at Make parse time using ``command -v <compiler>``.
* Dynamically generate targets using ``foreach`` expansions.
* Provide clean pattern rules for both compilation and execution.
* Expose ``check-<language>`` and ``check-<standard>`` targets.

Step 4: Annotate Security Threat Anchors
----------------------------------------

If your language includes constructs with potential safety hazards (for example, unchecked pointer arithmetic, non-local jumps, memory ordering relaxation, or variable-length stack allocations):

1. Tag the line in source code:

   .. code-block:: c

      /* [!SECURITY-NOTE: SEC-<ID>] Hazard description */

2. Document the anchor tag in ``<language>/security.rst`` with architectural causes, CWE mappings, and safe production alternatives.

Step 5: Verify Locally
----------------------

Verify your contribution locally against all supported compilers:

.. code-block:: bash

   make clean
   make check
   rstcheck --report-level warning README.rst CONTRIBUTING.rst docs/*.rst <language>/*.rst

Both the compiler verification harness and documentation linters must report zero warnings and zero errors.

Step 6: Submit via Your Preferred Platform
------------------------------------------

Omni accepts contributions on any of our primary and secondary git remotes:

* **GitLab Merge Requests (Canonical)**: Create a fork and submit an MR on `GitLab <https://gitlab.com/renich/omni/-/merge_requests>`_.
* **GitHub Pull Requests**: Create a fork and submit a PR on `GitHub <https://github.com/renich/omni/pulls>`_.
* **OpenLat Patches**: Push branches or submit patches via `OpenLat <https://git.openlat.dev/renich/omni>`_.

Commit and Pull Request Conventions
===================================

Commit Messages
---------------

Follow the Conventional Commits specification:

.. code-block:: text

   feat(<lang>): add <standard> reference implementation
   fix(<lang>): correct keyword saturation in <standard>
   docs(<lang>): document threat model in security.rst

Sign-Off and Co-Authorship
--------------------------

All commits must include a Developer Certificate of Origin (DCO) sign-off trailer:

.. code-block:: text

   Signed-off-by: Your Name <your.email@example.com>

If you paired with an AI assistant or peer developer, include the corresponding co-authorship trailer:

.. code-block:: text

   Co-authored-by: Assistant Name <assistant@example.com>

GPG Signing
-----------

Cryptographic signing is enabled and encouraged across the repository. Sign all commits using your GPG/SSH key:

.. code-block:: bash

   git commit -S -m "feat(lang): add reference implementation"

Financial Support and Donations
===============================

If you find omni valuable for your compiler engineering, syntax reference, or AI development workflows, financial contributions are gratefully accepted via `Liberapay <https://liberapay.com/Renich/donate>`_.
