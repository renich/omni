====
omni
====

The smallest piece of code that showcases the entirety of a programming language.

.. image:: https://gitlab.com/renich/omni/-/raw/master/assets/banner.svg
   :width: 100%
   :align: center
   :alt: Omni Project Banner

|

.. image:: https://gitlab.com/renich/omni/badges/master/pipeline.svg
   :target: https://gitlab.com/renich/omni/-/commits/master
   :alt: Pipeline Status
.. image:: https://img.shields.io/badge/GitLab_Pages-Live_Explorer-fc6d26?logo=gitlab&style=flat-square
   :target: https://renich.gitlab.io/omni/
   :alt: GitLab Pages Live Explorer
.. image:: https://img.shields.io/badge/Language-C_(C89_to_C23)-3b82f6?logo=c&style=flat-square
   :target: c/README.rst
   :alt: C Reference Suite
.. image:: https://img.shields.io/badge/Warnings-Zero_Pedantic-10b981?style=flat-square
   :target: GNUmakefile
   :alt: Zero Warnings
.. image:: https://img.shields.io/badge/Threat_Model-5_Anchors-e11d48?style=flat-square
   :target: c/security.rst
   :alt: Security Threat Model
.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg?logo=gnu&style=flat-square
   :target: LICENSE
   :alt: GNU General Public License v3
.. image:: https://img.shields.io/badge/Donate-Liberapay-f6c915.svg?logo=liberapay&logoColor=black&style=flat-square
   :target: https://liberapay.com/Renich/donate
   :alt: Donate using Liberapay

|

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

Repository Infrastructure
=========================

The canonical upstream repository is hosted on GitLab, with continuous mirrors on GitHub and OpenLat:

* **Primary Canonical Upstream**: `GitLab <https://gitlab.com/renich/omni>`_
* **Secondary Mirror, GitHub**: `GitHub <https://github.com/renich/omni>`_ (strict SHA-1 object format)
* **Secondary Mirror, OpenLat**: `OpenLat <https://git.openlat.dev/renich/omni>`_
* **Web UI and Code Browser**: `GitLab Pages <https://renich.gitlab.io/omni/>`_ | `GitHub Pages <https://renich.github.io/omni/>`_

Multi-Platform Contributions
============================

Omni is an open, community-driven effort to document every major programming language as executable ground truth. We warmly welcome contributions across any of our hosted platforms:

* **GitLab Merge Requests**: Open an MR directly on `GitLab <https://gitlab.com/renich/omni/-/merge_requests>`_
* **GitHub Pull Requests**: Submit a PR via `GitHub <https://github.com/renich/omni/pulls>`_
* **OpenLat Patches**: Push or send patches via `OpenLat <https://git.openlat.dev/renich/omni>`_

Whether you wish to contribute a modern C++ edition, a Zig or Crystal compendium, or implementations for Go, Rust, Python, or shell, your work is appreciated. Please review the `Contributing Guidelines <CONTRIBUTING.rst>`_ and the engineering lifecycle in the `Compendium Creation Process <docs/process.rst>`_ before submitting.

Quickstart and Verification
===========================

Verify all language implementations across detected compilers:

.. code-block:: bash

   make check

Verify an individual language or standard edition:

.. code-block:: bash

   make check-c
   make check-c23

Build the static documentation site and interactive code browser:

.. code-block:: bash

   make site

Documentation
=============

Detailed architectural guidelines, standard compendiums, and contribution instructions are maintained in dedicated reference documents:

* `Language Standards and Roadmap <docs/standards.rst>`_: Full matrix of verified language editions, toolchain baselines, and prospective roadmap targets.
* `C Reference Suite <c/README.rst>`_: C language standards matrix, compiler baselines, and execution notes.
* `C Security Threat Model <c/security.rst>`_: Threat model catalog and security advisories for hazardous C features.
* `Repository Architecture <docs/architecture.rst>`_: Repository layout, naming conventions, and build system invariants.
* `Compendium Creation Process <docs/process.rst>`_: Detailed 6-phase engineering lifecycle for authoring compendiums.
* `Contributing Guidelines <CONTRIBUTING.rst>`_: Contribution requirements, workflow, and submission checklist.
* `Changelog <CHANGELOG.rst>`_: Project version history and changelog.
* `AI Agent Directive <AGENTS.md>`_: Machine directives and operating constraints for autonomous AI coding agents.

License
=======

This project is free software licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later). See the `LICENSE <LICENSE>`_ file for details.
