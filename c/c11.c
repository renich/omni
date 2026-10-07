/*
 * omni: c11.c
 * Canonical, exhaustive ISO/IEC 9899:2011 (C11) language compendium.
 * Build: $(CC) -std=c11 -Wall -Wextra -pedantic -Werror -pthread c11.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <uchar.h>
#include <complex.h>
#include <stdatomic.h>
#include <stdalign.h>
#include <stdnoreturn.h>
#include <inttypes.h>
#include <fenv.h>
#include <stdarg.h>
#include <setjmp.h>
#include <signal.h>
#include <math.h>

/*
 * Section 1: Preprocessor Directives (ISO C11 Clause 6.10)
 */

#define STR_EXPAND(x) #x
#define STR(x) STR_EXPAND(x)
#define GLUE(a, b) a ## b
#define LOG_MSG(fmt, ...) printf(fmt, __VA_ARGS__)

#undef OMNI_UNDEFINED
#define OMNI_C11_ACTIVE 1

#if __STDC_VERSION__ != 201112L
#  error "Strict ISO C11 compliance required"
#endif

#if defined(OMNI_C11_ACTIVE)
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
_Pragma("message(\"Omni: Verifying ISO C11 Language Construct Compliance\")")
#if defined(__clang__)
#  pragma clang diagnostic pop
#endif

/*
 * Section 2: Assertions, Atomics, Alignment, and Types (Clause 6.7)
 */

/*
 * Dual-Path Saturation Pattern (ISO C11 Clause 6.7.2):
 * Optional normative keyword _Imaginary (Annex G)
 */
#ifdef __STDC_IEC_559_COMPLEX__
/* Annex G Imaginary types supported */
#else
#  if 0
typedef _Imaginary double imag_ref;
#  endif
#endif

// In C11, _Static_assert requires two arguments
_Static_assert(__STDC_VERSION__ == 201112L, "C11 version verification");
_Static_assert(sizeof(int32_t) == 4, "int32_t must be 4 bytes");

// Alignment specifiers
struct AlignedBlock {
    _Alignas(16) uint8_t simd_buffer[16];
    alignas(double) char aligned_as_double;
};

// Anonymous structure and union members
struct Container {
    union {
        int id;
        float alt_id;
    };
    struct {
        uint16_t sub_code;
        double precision;
    };
};

struct DynamicPacket {
    size_t length;
    int payload[]; // Flexible array member
};

// [!SECURITY-NOTE: SEC-BITFIELD-01] Implementation-defined bitfield packing & signedness
struct BitFields {
    unsigned int flag_a : 1;
    unsigned int flag_b : 1;
    unsigned int        : 2; // Unnamed padding
    unsigned int        : 0; // Boundary alignment
    unsigned int val    : 4;
};

// _Noreturn function specifier
_Noreturn static void fatal_abort(void) {
    exit(EXIT_FAILURE);
}

// C11 generic selection macro
#define TYPE_NAME(x) _Generic((x), \
    bool: "bool", \
    char: "char", \
    int: "int", \
    long: "long", \
    float: "float", \
    double: "double", \
    default: "other")

inline static int math_square(int x) {
    return x * x;
}

void matrix_worker(int rows, int cols, double matrix[*][*]);

void matrix_worker(int rows, int cols, double matrix[rows][cols]) {
    if (rows > 0 && cols > 0) matrix[0][0] = 42.0;
}

static void qualified_consumer(int buffer[static restrict 4]) {
    buffer[0] += 1;
}

static int static_triplet[3] = {10, 20, 30};

static int (*array_provider(void))[3] {
    return &static_triplet;
}

typedef int (*(*array_provider_fn)(void))[3];
typedef int (*binary_op_fn)(int, int);

static int op_multiply(int a, int b) { return a * b; }
static binary_op_fn dispatch_table[1] = { op_multiply };

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

static void sigint_handler(int sig) {
    (void)sig;
}

// [!SECURITY-NOTE: SEC-JMP-01] Non-local jumps bypass stack unwinding and clobber registers
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
    auto int legacy_auto = 1;
    register int fast_counter = 0;
    static unsigned long run_counter = 0;

    // C11 Thread-local storage specifiers
    _Thread_local static int tls_var = 10;

    // Scalar types
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

    int32_t exact_32 = INT32_C(-100);
    uint64_t exact_u64 = UINT64_C(200);

    bool active_flag = true;
    active_flag = false;
    _Bool legacy_bool_flag = 1;

    float dec_float = 1.25e-2f;
    double reg_double = 3.1415926535;
    long double ext_double = 2.718281828L;
    double hex_float = 0x1.0p-3;

    float complex complex_f = 1.0f + 2.0f * I;
    double _Complex complex_d = 3.0 + 4.0 * I;

    // Unicode characters and strings (C11 uchar.h)
    char c_ascii = 'A';
    wchar_t c_wide = L'Ω';
    char16_t c_u16 = u'ñ';
    char32_t c_u32 = U'Ψ';
    const char *s_ascii = "ISO C11 Literal";
    const wchar_t *s_wide = L"Wide String";
    const char16_t *s_u16 = u"UTF-16 String";
    const char32_t *s_u32 = U"UTF-32 String";
    const char *s_u8 = u8"UTF-8 String";

    // Qualifiers and atomics
    const volatile int hw_reg = 0xBEEF;
    const volatile int *ptr_hw = &hw_reg;
    int memory_target = 10;
    int *const const_p = &memory_target;
    int *restrict restrict_p = &memory_target;

    // [!SECURITY-NOTE: SEC-ATOMIC-01] Relaxed atomic operations lack synchronization barriers
    _Atomic int atomic_counter = ATOMIC_VAR_INIT(0);
    _Atomic(uint32_t) atomic_wrapped = 100U;
    atomic_flag atomic_spin = ATOMIC_FLAG_INIT;

    atomic_init(&atomic_counter, 1);
    atomic_fetch_add_explicit(&atomic_counter, 2, memory_order_relaxed);
    atomic_store_explicit(&atomic_wrapped, 200U, memory_order_release);
    bool spin_acquired = !atomic_flag_test_and_set(&atomic_spin);
    if (spin_acquired) {
        atomic_flag_clear(&atomic_spin);
    }

    // Alignment operators
    size_t align_c11_a = _Alignof(struct AlignedBlock);
    size_t align_c11_b = alignof(struct AlignedBlock);

    // Designated initializers and compound literals
    int sparse_arr[5] = { [1] = 11, [3] = 33 };
    struct Container cont = { .id = 100, .sub_code = 12, .precision = 3.14 };
    struct BitFields bit_unit = { .flag_a = 1, .flag_b = 0, .val = 7 };

    int *compound_arr = (int[]){ 10, 20, 30 };
    struct Container compound_cont = (struct Container){ .id = 200, .sub_code = 24 };

    // [!SECURITY-NOTE: SEC-VLA-01] Block scope VLA object (stack exhaustion hazard)
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

    int GLUE(symbolic_, var) = 777;
    const char *current_fn = __func__;

    int op_x = 20, op_y = 6;
    int arithmetic = ((op_x + op_y) * 2 - (op_x / op_y) + (op_x % op_y));
    int bitwise = ((op_x << 2) >> 1) ^ (~op_y & (op_x | 0x0F));
    bool logical = (op_x > op_y) && (op_x >= 20) && (op_y < 10) && (op_y <= 6) && (op_x != op_y);
    int ternary = logical ? (bit_unit.flag_a ? 100 : 200) : 300;
    int comma_res = (fast_counter++, fast_counter + 5);

    arithmetic += 1; arithmetic -= 1; arithmetic *= 2; arithmetic /= 2; arithmetic %= 100;
    bitwise &= 0xFF; bitwise ^= 0x0F; bitwise |= 0x10; bitwise <<= 1; bitwise >>= 1;

    enum { STATE_INIT, STATE_WORK, STATE_DONE } state = STATE_WORK;

    if (ternary == 100 && (state == STATE_WORK)) {
        goto target_label;
    } else {
        while (false) {}
    }

target_label:
    do {
        switch (state) {
            case STATE_INIT:
                run_counter++;
                // Fallthrough
            case STATE_WORK:
                for (int i = 0; i < 3; i++) {
                    if (i == 0) continue;
                    run_counter++;
                    if (i == 2) break;
                }
                break;
            case STATE_DONE:
                break;
            default:
                fatal_abort();
        }
    } while (0);

    if (ternary == 999) goto end_control_label;
end_control_label: ;

    int jump_res = execute_nonlocal_jump();
    signal(SIGINT, sigint_handler);
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
    printf("C11 check: Type=%s | Square=%d | Sum=%d | Triplet=%d | Dispatch=%d | Runs=%lu\n",
           TYPE_NAME(s_int), math_square(4), var_sum, triplet_val, dispatch_res, run_counter);

    long double checksum =
        (long double)legacy_auto + fast_counter + run_counter + *ptr_hw + *const_p + *restrict_p +
        s_char + u_char + s_short + u_short + s_int + u_int + s_long + u_long +
        (s_llong + u_llong) + exact_32 + exact_u64 + (active_flag ? 1 : 0) + (legacy_bool_flag ? 1 : 0) +
        dec_float + reg_double + ext_double + hex_float +
        creal(complex_f) + cimag(complex_d) + c_ascii + (int)c_wide + (int)c_u16 + (int)c_u32 +
        s_ascii[0] + (int)s_wide[0] + (int)s_u16[0] + (int)s_u32[0] + s_u8[0] +
        atomic_counter + atomic_wrapped + (spin_acquired ? 1 : 0) +
        align_c11_a + align_c11_b + sparse_arr[1] + cont.id + bit_unit.val +
        compound_arr[0] + compound_cont.id + vla_storage[0] + symbolic_var +
        arithmetic + bitwise + (logical ? 1 : 0) + ternary + comma_res +
        (int)state + jump_res + triplet_val + dispatch_res + test_matrix[0][0] +
        test_seq[0] + var_sum + external_symbol + CONFIG_FLAG + tls_var;

    if (isnan((double)checksum)) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
