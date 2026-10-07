CC ?= gcc
CLANG ?= clang
LDFLAGS ?= -lm
PTHREAD ?= -pthread

BUILD_DIR := build

C_STANDARDS := c89 c99 c11 c17 c23

# Compiler flags per standard
CFLAGS_c89 := -std=c89 -Wall -Wextra -pedantic -Werror
CFLAGS_c99 := -std=c99 -Wall -Wextra -pedantic -Werror
CFLAGS_c11 := -std=c11 -Wall -Wextra -pedantic -Werror $(PTHREAD)
CFLAGS_c17 := -std=c17 -Wall -Wextra -pedantic -Werror $(PTHREAD)
CFLAGS_c23 := -std=c23 -Wall -Wextra -pedantic -Werror $(PTHREAD)

all: check

$(BUILD_DIR):
	mkdir -p $@

# Pattern rules for GCC and Clang builds
define make_c_targets
$$(BUILD_DIR)/$(1)_gcc: c/$(1).c | $$(BUILD_DIR)
	$$(CC) $$(CFLAGS_$(1)) $$< $$(LDFLAGS) -o $$@

$$(BUILD_DIR)/$(1)_clang: c/$(1).c | $$(BUILD_DIR)
	@if command -v $$(CLANG) >/dev/null 2>&1; then \
		$$(CLANG) $$(CFLAGS_$(1)) $$< $$(LDFLAGS) -o $$@; \
	fi

check-$(1): $$(BUILD_DIR)/$(1)_gcc $$(BUILD_DIR)/$(1)_clang
	@echo "==> Verifying $(1) (GCC)..."
	./$$(BUILD_DIR)/$(1)_gcc
	@if [ -f $$(BUILD_DIR)/$(1)_clang ]; then \
		echo "==> Verifying $(1) (Clang)..."; \
		./$$(BUILD_DIR)/$(1)_clang; \
	fi
	@echo "==> $(1) verification passed."
endef

$(foreach std,$(C_STANDARDS),$(eval $(call make_c_targets,$(std))))

check-c: $(addprefix check-,$(C_STANDARDS))
	@echo "==> All C standards (C89, C99, C11, C17, C23) verified successfully."

check: check-c

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all check check-c clean $(addprefix check-,$(C_STANDARDS))
