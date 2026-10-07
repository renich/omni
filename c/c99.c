/*
 * omni: c99.c
 * Canonical, exhaustive ISO/IEC 9899:1999 (C99) language compendium.
 * Build: $(CC) -std=c99 -Wall -Wextra -pedantic -Werror c99.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <inttypes.h>
#include <complex.h>
#include <fenv.h>
#include <stdarg.h>
#include <setjmp.h>
#include <signal.h>
#include <math.h>

/*
 * Section 1: Preprocessor Directives (ISO C99 Clause 6.10)
 */

#define STR_EXPAND(x) #x
#define STR(x) STR_EXPAND(x)
#define GLUE(a, b) a ## b
#define LOG_MSG(fmt, ...) printf(fmt, __VA_ARGS__)

#undef OMNI_UNDEFINED
#define OMNI_C99_ACTIVE 1

#if __STDC_VERSION__ != 199901L
#  error "Strict ISO C99 compliance required"
#endif

#if defined(OMNI_C99_ACTIVE)
#  define CONFIG_FLAG 1
#elif !defined(OMNI_UNDEFINED)
#  error "Unreachable branch"
#else
#  error "Unreachable branch"
#endif

#if defined(__clang__)
#  pragma clang diagnostic push
#  pragma clang diagnostic ignored "-W#pragma-messages"
#endif
_Pragma("message(\"Omni: Verifying ISO C99 Language Construct Compliance\")")
#if defined(__clang__)
#  pragma clang diagnostic pop
#endif

/*
 * Section 2: Declarations, Structs, VLAs, Inlines, Qualifiers (Clause 6.7)
 */

enum Status {
    STATUS_INIT = 0,
    STATUS_WORK = 1,
    STATUS_DONE = 2, // C99 allows trailing comma in enum
};

struct DynamicPacket {
    size_t length;
    int payload[]; // Flexible array member
};

struct BitFields {
    unsigned int flag_a : 1;
    unsigned int flag_b : 1;
    unsigned int        : 2; // Unnamed padding
    unsigned int        : 0; // Boundary alignment
    unsigned int val    : 4;
};

// C99 inline function
inline static int math_square(int x) {
    return x * x;
}

// Function prototype with variable-length array dimension indicator [*]
void matrix_worker(int rows, int cols, double matrix[*][*]);

void matrix_worker(int rows, int cols, double matrix[rows][cols]) {
    if (rows > 0 && cols > 0) matrix[0][0] = 42.0;
}

// Array parameter qualified with static and restrict
static void qualified_consumer(int buffer[static restrict 4]) {
    buffer[0] += 1;
}

// Pointer to array and complex function pointer types
static int static_triplet[3] = {10, 20, 30};

static int (*array_provider(void))[3] {
    return &static_triplet;
}

typedef int (*(*array_provider_fn)(void))[3];
typedef int (*binary_op_fn)(int, int);

static int op_multiply(int a, int b) {
    return a * b;
}

static binary_op_fn dispatch_table[1] = { op_multiply };

// Variadic function conforming to C99
static int sum_variadic(size_t count, ...) {
    va_list ap;
    int total = 0;
    va_start(ap, count);
    for (size_t i = 0; i < count; i++) {
        total += va_arg(ap, int);
    }
    va_end(ap);
    return total;
}

static jmp_buf nonlocal_buf;
extern int external_symbol;
int external_symbol = 42;

static void sigusr_handler(int sig) {
    (void)sig;
}

static int execute_nonlocal_jump(void) {
    volatile int jump_performed = 0;
    if (setjmp(nonlocal_buf) == 0) {
        if (!jump_performed) {
            jump_performed = 1;
            longjmp(nonlocal_buf, 1);
        }
    }
    return jump_performed;
}

int main(void) {
    // In C99, declarations can mix with code
    auto int legacy_auto = 1;
    register int fast_counter = 0;
    static unsigned long run_counter = 0;

    // Standard scalar types
    signed char s_char = -12;
    unsigned char u_char = 255U;
    short s_short = -32767;
    unsigned short u_short = 65535U;
    int s_int = -2147483647;
    unsigned int u_int = 4294967295U;
    long s_long = -2147483647L;
    unsigned long u_long = 4294967295UL;
    long long s_llong = -9223372036854775807LL;
    unsigned long long u_llong = 18446744073709551615ULL;

    // Exact-width integers from stdint.h
    int32_t exact_32 = INT32_C(-100);
    uint64_t exact_u64 = UINT64_C(200);

    // Boolean type
    bool active_flag = true;
    active_flag = false;

    // Floating-point representations
    float dec_float = 1.25e-2f;
    double reg_double = 3.1415926535;
    long double ext_double = 2.718281828L;
    double hex_float = 0x1.0p-3; // C99 hexadecimal floating-point

    // Complex numbers from complex.h
    float complex complex_f = 1.0f + 2.0f * I;
    double _Complex complex_d = 3.0 + 4.0 * I;

    // Character and string literals
    char c_ascii = 'A';
    wchar_t c_wide = L'Z';
    const char *s_ascii = "ISO C99 Literal";
    const wchar_t *s_wide = L"Wide String";

    // Qualifiers
    const volatile int hw_reg = 0xBEEF;
    const volatile int *ptr_hw = &hw_reg;
    int memory_target = 10;
    int *const const_p = &memory_target;
    int *restrict restrict_p = &memory_target;

    // C99 Designated initializers
    int sparse_arr[5] = { [1] = 11, [3] = 33 };
    struct BitFields bit_unit = { .flag_a = 1, .flag_b = 0, .val = 7 };

    // C99 Compound literals
    int *compound_arr = (int[]){ 10, 20, 30 };
    struct BitFields compound_bf = (struct BitFields){ .flag_a = 0, .flag_b = 1, .val = 3 };

    // Variable length array in block scope
    size_t vla_len = (size_t)(fast_counter + 3);
    int vla_storage[vla_len];
    vla_storage[0] = math_square(5);

    // Flexible array member allocation
    struct DynamicPacket *packet = malloc(sizeof(struct DynamicPacket) + (sizeof(int) * 2));
    if (packet) {
        packet->length = 2;
        packet->payload[0] = 0x11;
        packet->payload[1] = 0x22;
        free(packet);
    }

    // Preprocessor token pasting and __func__
    int GLUE(symbolic_, var) = 777;
    const char *current_fn = __func__;

    // Operators and precedence
    int op_x = 20, op_y = 6;
    int arithmetic = ((op_x + op_y) * 2 - (op_x / op_y) + (op_x % op_y));
    int bitwise = ((op_x << 2) >> 1) ^ (~op_y & (op_x | 0x0F));
    bool logical = (op_x > op_y) && (op_x >= 20) && (op_y < 10) && (op_y <= 6) && (op_x != op_y);
    int ternary = logical ? (bit_unit.flag_a ? 100 : 200) : 300;
    int comma_res = (fast_counter++, fast_counter + 5);

    arithmetic += 1; arithmetic -= 1; arithmetic *= 2; arithmetic /= 2; arithmetic %= 100;
    bitwise &= 0xFF; bitwise ^= 0x0F; bitwise |= 0x10; bitwise <<= 1; bitwise >>= 1;

    // Control flow
    enum Status state = STATUS_WORK;

    if (ternary == 100 && (state == STATUS_WORK)) {
        goto target_label;
    } else {
        while (false) {}
    }

target_label:
    do {
        switch (state) {
            case STATUS_INIT:
                run_counter++;
                // Fallthrough
            case STATUS_WORK:
                // C99 for-loop variable declaration
                for (int i = 0; i < 3; i++) {
                    if (i == 0) continue;
                    run_counter++;
                    if (i == 2) break;
                }
                break;
            case STATUS_DONE:
                break;
            default:
                exit(EXIT_FAILURE);
        }
    } while (0);

    if (ternary == 999) goto end_control_label;
end_control_label: ;

    int jump_res = execute_nonlocal_jump();
    signal(SIGUSR1, sigusr_handler);
    feclearexcept(FE_ALL_EXCEPT);

    array_provider_fn provider = array_provider;
    int (*resolved_triplet)[3] = provider();
    int triplet_val = (*resolved_triplet)[1];

    int dispatch_res = dispatch_table[0](10, 5);

    double test_matrix[2][2] = { {0.0, 0.0}, {0.0, 0.0} };
    matrix_worker(2, 2, test_matrix);

    int test_seq[4] = {1, 2, 3, 4};
    qualified_consumer(test_seq);

    int var_sum = sum_variadic(3, 10, 20, 30);

    LOG_MSG("File: %s | Line: %d | Func: %s | Symbol: %d\n",
            __FILE__, __LINE__, current_fn, symbolic_var);
    printf("C99 check: Square=%d | Sum=%d | Triplet=%d | Dispatch=%d | Runs=%lu\n",
           math_square(4), var_sum, triplet_val, dispatch_res, run_counter);

    long double checksum =
        (long double)legacy_auto + fast_counter + run_counter + *ptr_hw + *const_p + *restrict_p +
        s_char + u_char + s_short + u_short + s_int + u_int + s_long + u_long +
        (s_llong + u_llong) + exact_32 + exact_u64 + (active_flag ? 1 : 0) +
        dec_float + reg_double + ext_double + hex_float +
        creal(complex_f) + cimag(complex_d) + c_ascii + (int)c_wide + s_ascii[0] + (int)s_wide[0] +
        sparse_arr[1] + bit_unit.val + compound_arr[0] + compound_bf.val +
        vla_storage[0] + symbolic_var + arithmetic + bitwise + (logical ? 1 : 0) +
        ternary + comma_res + (int)state + jump_res + triplet_val + dispatch_res +
        test_matrix[0][0] + test_seq[0] + var_sum + external_symbol + CONFIG_FLAG;

    if (isnan((double)checksum)) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
