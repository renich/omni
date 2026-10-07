# GNUmakefile for omni
SHELL       := /usr/bin/bash
.SHELLFLAGS := -euo pipefail -c
.DELETE_ON_ERROR:

BUILD_DIR := build
SRC_DIR   := c
STANDARDS := c89 c99 c11 c17 c23

# 1. Parse-time Compiler Detection (Prevents phantom target idempotency bugs)
COMPILERS :=
ifneq ($(shell command -v gcc 2>/dev/null),)
	COMPILERS += gcc
endif
ifneq ($(shell command -v clang 2>/dev/null),)
	COMPILERS += clang
endif

ifeq ($(COMPILERS),)
	$(error No C compilers (gcc or clang) found in PATH)
endif

# 2. Matrix Target Generation
# Targets: build/c89_gcc build/c89_clang build/c99_gcc ...
TARGETS := $(foreach std,$(STANDARDS),$(foreach comp,$(COMPILERS),$(BUILD_DIR)/$(std)_$(comp)))

# 3. Compiler Flags
# -I$(SRC_DIR) guarantees #embed and headers resolve portably regardless of invocation context
CFLAGS_BASE := -Wall -Wextra -pedantic -Werror -I$(SRC_DIR)
LDFLAGS     := -lm

# Thread flags for C11, C17, and C23
THREAD_FLAG_c89 :=
THREAD_FLAG_c99 :=
THREAD_FLAG_c11 := -pthread
THREAD_FLAG_c17 := -pthread
THREAD_FLAG_c23 := -pthread

all: check

$(BUILD_DIR):
	mkdir -p $@

# 4. Static Pattern Rules mapped dynamically by standard ($*)
$(filter %_gcc,$(TARGETS)): $(BUILD_DIR)/%_gcc: $(SRC_DIR)/%.c | $(BUILD_DIR)
	gcc -std=$* $(CFLAGS_BASE) $(THREAD_FLAG_$*) $< $(LDFLAGS) -o $@

$(filter %_clang,$(TARGETS)): $(BUILD_DIR)/%_clang: $(SRC_DIR)/%.c | $(BUILD_DIR)
	clang -std=$* $(CFLAGS_BASE) $(THREAD_FLAG_$*) $< $(LDFLAGS) -o $@

# 5. Verification Harness
check-c: $(TARGETS)
	@echo "==> Running verification test suite across all detected compilers ($(COMPILERS))..."
	@for target in $(TARGETS); do \
		echo "--> Executing $$target ..."; \
		./$$target >/dev/null || exit 1; \
	done
	@echo "==> All C standards verified cleanly across compilers: $(COMPILERS)"

define make_check_standard
check-$(1): $$(filter $$(BUILD_DIR)/$(1)_%,$$(TARGETS))
	@for target in $$^; do \
		echo "--> Executing $$$$target ..."; \
		./$$$$target >/dev/null || exit 1; \
	done
	@echo "==> $(1) verification passed."
endef

$(foreach std,$(STANDARDS),$(eval $(call make_check_standard,$(std))))

# 6. Documentation Linter
RST_FILES := $(shell find . -name "*.rst" -not -path "./.git/*")
check-docs:
	@if command -v rstcheck >/dev/null 2>&1; then \
		echo "==> Verifying documentation syntax with rstcheck..."; \
		rstcheck --report-level warning $(RST_FILES); \
		echo "==> Documentation syntax verified cleanly."; \
	else \
		echo "[omni] rstcheck not found in PATH; skipping documentation check."; \
	fi

check: check-c check-docs

# 7. AI Agent Rule Synchronization
agent-rules:
	@echo "==> Synchronizing AI agent rules..."
	@cat .agents/rules/*.md > .cursorrules
	@cp .cursorrules CLAUDE.md
	@cp .cursorrules .windsurfrules
	@echo "==> AI agent rules synchronized (.cursorrules, CLAUDE.md, .windsurfrules)."

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all check check-c check-docs agent-rules clean $(addprefix check-,$(STANDARDS))
