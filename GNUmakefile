CC ?= gcc
CLANG ?= clang
CFLAGS ?= -std=c23 -Wall -Wextra -pedantic -Werror -pthread
LDFLAGS ?= -lm

BUILD_DIR := build
BIN_C23_GCC := $(BUILD_DIR)/c23_gcc
BIN_C23_CLANG := $(BUILD_DIR)/c23_clang

all: check

$(BUILD_DIR):
	mkdir -p $@

$(BIN_C23_GCC): c/c23.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

$(BIN_C23_CLANG): c/c23.c | $(BUILD_DIR)
	@if command -v $(CLANG) >/dev/null 2>&1; then \
		$(CLANG) $(CFLAGS) $< $(LDFLAGS) -o $@; \
	fi

check-c: $(BIN_C23_GCC) $(BIN_C23_CLANG)
	@echo "==> Running c23 binary (GCC)..."
	./$(BIN_C23_GCC)
	@if [ -f $(BIN_C23_CLANG) ]; then \
		echo "==> Running c23 binary (Clang)..."; \
		./$(BIN_C23_CLANG); \
	fi
	@echo "==> C23 verification complete."

check: check-c

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all check check-c clean
