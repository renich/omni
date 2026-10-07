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

Repository Infrastructure
=========================

The canonical upstream repository is hosted on GitLab. All merge requests, issue tracking, and primary maintenance occur there:

* **Primary Canonical Upstream**: `GitLab <https://gitlab.com/renich/omni>`_
* **Secondary Mirror, GitHub**: `GitHub <https://github.com/renich/omni>`_ (strict SHA-1 object format)
* **Secondary Mirror, OpenLat**: `OpenLat <https://git.openlat.dev/renich/omni>`_
* **Web UI and Code Browser**: `GitLab Pages <https://omni-b7ef04.gitlab.io/>`_ | `GitHub Pages <https://renich.github.io/omni/>`_

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

* :doc:`docs/standards`: Full matrix of verified language editions, toolchain baselines, and prospective roadmap targets.
* :doc:`c/README`: C language standards matrix, compiler baselines, and execution notes.
* :doc:`c/security`: Threat model catalog and security advisories for hazardous C features.
* :doc:`docs/architecture`: Repository layout, naming conventions, and build system invariants.
* :doc:`docs/process`: Detailed 6-phase engineering lifecycle for authoring compendiums.
* :doc:`CONTRIBUTING`: Contribution requirements, workflow, and submission checklist.
* :doc:`CHANGELOG`: Project version history and changelog.
* ``AGENTS.md``: Machine directives and operating constraints for autonomous AI coding agents.
