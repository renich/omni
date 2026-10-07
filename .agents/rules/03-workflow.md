# Workflow and Verification Guardrails

## 1. Multi-Toolchain Verification

Always execute the verification suite before proposing or committing changes:

```bash
make clean
make check
```

The build must pass with exit code `0` across all detected compilers without generating any warnings.

## 2. Documentation Standards

- All human-facing documentation files (`README.rst`, `docs/*.rst`, `c/*.rst`) are strictly ReStructuredText (`.rst`).
- Always verify ReST syntax using:
  ```bash
  make check-docs
  ```
- Never generate Markdown tables or backtick code blocks inside `.rst` files.
- Agent rule files (`AGENTS.md` and `.agents/rules/*.md`) are the only Markdown files allowed.

## 3. Git Commits and Attribution

- Adhere to Conventional Commits: `feat(<scope>): description`, `fix(<scope>): description`, `docs(<scope>): description`.
- Include DCO sign-off:
  ```text
  Signed-off-by: Rénich Bon Ćirić <renich@evalinux.com>
  ```
- Include AI co-authorship trailer:
  ```text
  Co-authored-by: Antigravity <antigravity@google.com>
  ```
- Ensure commits are GPG-signed.
