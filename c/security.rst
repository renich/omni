================================================
C Language Security and Hazardous Feature Matrix
================================================

Operational threat model and hazard advisory for C language constructs demonstrated in omni.

Executive Summary
=================

The ``omni`` C suite (``c89.c`` through ``c23.c``) serves as an exhaustive syntactic reference and compiler saturator. To demonstrate 100% of the language, these files deliberately exercise historical, implementation-defined, and memory-hazardous constructs.

This code is an executable syntax compendium; it is not hardened production software. When using ``omni`` for syntax reference, never copy hazardous constructs into production systems without defensive architectural controls.

Threat Model Index
==================

.. list-table::
   :widths: 20 25 25 30
   :header-rows: 1

   * - Anchor Tag
     - Affected Standards
     - Primary Vulnerability
     - Defensive Production Recommendation

   * - ``SEC-VLA-01``
     - C99, C11, C17, C23
     - Stack exhaustion / denial of service (CWE-400, CWE-770)
     - Use fixed-size buffers or bounded dynamic allocation (``malloc``) with integer overflow checks.

   * - ``SEC-JMP-01``
     - C89, C99, C11, C17, C23
     - Register clobbering, stack unwinding bypass, resource leakage
     - Replace ``setjmp``/``longjmp`` with explicit error return codes and structured status propagation.

   * - ``SEC-C89-UNBOUNDED-01``
     - C89
     - Classic buffer overflow via unbounded string utilities (CWE-120)
     - Prohibit ``strcpy``/``strcat``; enforce bounded alternatives or Annex K bounds-checking interfaces.

   * - ``SEC-BITFIELD-01``
     - C89, C99, C11, C17, C23
     - Implementation-defined allocation unit ordering and signedness ambiguity
     - Avoid bitfields for wire protocols or IPC; use explicit bitwise masking over fixed-width unsigned types.

   * - ``SEC-ATOMIC-01``
     - C11, C17, C23
     - Data races and out-of-order execution via relaxed memory ordering
     - Default to sequential consistency (``memory_order_seq_cst``) unless formal memory models prove correctness.

Detailed Hazard Analysis
========================

Variable-Length Arrays: SEC-VLA-01
----------------------------------

* **Mechanism**: Dynamic stack allocation based on runtime dimensions (``int arr[n];``).
* **Hazard**: Stack overflow cannot be intercepted in standard C; supplying an unvalidated or oversized integer triggers immediate segmentation faults or stack clash exploits.
* **Standard Evolution**: C99 introduced VLAs as mandatory. C11 and C17 made VLA objects optional (conditional on ``__STDC_NO_VLA__``). C23 preserves variably modified (VM) pointer types (``int (*p)[n]``) while keeping VLA stack objects optional.
* **Industry Mandates**: Fully banned in the Linux Kernel, Google C++ Style Guide, and MISRA C:2023 Rule 18.8.

Non-Local Jumps: SEC-JMP-01
---------------------------

* **Mechanism**: Direct context restoration across stack frames using ``setjmp`` and ``longjmp``.
* **Hazard**: Local non-volatile variables modified between ``setjmp`` and ``longjmp`` contain indeterminate values upon jump completion. Furthermore, non-local jumps bypass cleanup handlers, mutex unlocking, and file descriptor closure.
* **Remediation**: Use structured return values (e.g. error enumeration or status struct) and handle unwind logic explicitly.

Unbounded Buffer Operations: SEC-C89-UNBOUNDED-01
-------------------------------------------------

* **Mechanism**: Unbounded string copy operations (e.g. ``strcpy``, ``strcat``, ``sprintf``).
* **Hazard**: Destination buffer overrun when input lengths exceed fixed capacities.
* **Remediation**: In modern C code, enforce strict length validation, size-bounded routines, or dynamic allocation with explicit bounds checks.

Bitfield Portability: SEC-BITFIELD-01
-------------------------------------

* **Mechanism**: Packing multiple logical flags into partial integer storage units.
* **Hazard**: The order of bit allocation within storage units (high-to-low or low-to-high) is implementation-defined. Plain ``int`` bitfields may be signed or unsigned depending on the compiler ABI.
* **Remediation**: For serialization or hardware register mapping, use unsigned fixed-width types (``uint32_t``) and explicit shift/mask operators.

Relaxed Atomics: SEC-ATOMIC-01
------------------------------

* **Mechanism**: Atomic operations using ``memory_order_relaxed``.
* **Hazard**: Relaxed ordering provides atomicity but zero synchronization or instruction ordering guarantees across threads.
* **Remediation**: Use ``memory_order_acquire``, ``memory_order_release``, or ``memory_order_seq_cst`` to enforce memory barriers across concurrent execution contexts.

Production Toolchain Hardening
==============================

When compiling C for production deployments, enforce the following baseline compiler hardening flags:

.. code-block:: bash

   # GCC / Clang hardening baseline
   CFLAGS += -fstack-protector-strong -D_FORTIFY_SOURCE=3 -fPIE -Wformat=2 -Wformat-security
   LDFLAGS += -Wl,-z,relro -Wl,-z,now -pie

   # Dynamic analysis during automated testing
   CFLAGS_TEST := -fsanitize=address,undefined -fno-omit-frame-pointer
