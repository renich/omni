# Architectural Invariants

Every AI agent operating in omni must strictly adhere to the following non-negotiable invariants:

1. **Single-File Self-Containment**:
   - Zero auxiliary local headers or multi-file dependencies.
   - Only standard library headers defined by the normative language specification are permitted.
2. **Pedantic Compilation Purity**:
   - Must compile with zero warnings under `-Wall -Wextra -pedantic -Werror` (or language-equivalent pedantic flags).
   - Never suppress compiler warnings using ad-hoc compiler flags.
3. **100% Lexical and Keyword Saturation**:
   - Every normative keyword, standard type, and operator from the target language specification must appear and be syntactically or functionally evaluated.
   - Retained keywords (e.g. `_Bool` in C23) must be present.
4. **Git Object Format**:
   - The repository object format is strictly SHA-1 for GitHub mirror compatibility.
   - Never attempt to upgrade or alter the git object database to SHA-256.
5. **Executable Ground Truth**:
   - Every file must compile into an executable binary that completes execution and exits with status code `0`.
