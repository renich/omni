# Required Design Patterns

## 1. Scalar State Accumulator Pattern

Never use `(void)x;` or `#pragma` suppression lines to silence `unused-variable` warnings. All declared scalar variables, function return values, and type instantiations must be mathematically consumed into a single unified state accumulator:

- **Prohibited pattern**:
  ```c
  int a = 5;
  (void)a; /* Prohibited dead suppression */
  ```
- **Mandatory pattern**:
  ```c
  double checksum = (double)legacy_auto + fast_counter + *ptr_hw +
                    s_char + u_char + dec_float + reg_double +
                    c_ascii + record_inst.flags.val + symbolic_var;
  if (checksum < 0.0) {
      return 1;
  }
  ```

## 2. Dual-Path Saturation Pattern

For optional language annexes, conditionally supported extensions, or compiler-dependent intrinsics (e.g. Annex G `_Imaginary` or Annex F/H Decimal Floating Point):

- Active path: If the toolchain macro indicates support, exercise the feature at runtime.
- Inactive fallback: If unsupported, place declarations inside an `#else` block (or `#if 0`) so the keywords remain physically present in the source text for saturation scanning without causing compilation failure under `-Werror`.

```c
#ifdef __STDC_IEC_60559_DFP__
static _Decimal32  active_d32  = 1.0DF;
#else
#  if 0
typedef _Decimal32  d32_ref;
#  endif
#endif
```

## 3. Bidirectional Security Threat Anchors

Whenever code exercises historically hazardous, memory-unsafe, or implementation-defined features:

1. Annotate the line with an inline tag:
   ```c
   /* [!SECURITY-NOTE: SEC-<ID>] Hazard explanation */
   ```
2. Ensure the ID is cataloged in the language directory's `security.rst` with architectural analysis, CWE mapping, and safe production alternatives.
