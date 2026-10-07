/*
 * omni: c23.c
 * Canonical, exhaustive ISO/IEC 9899:2024 (C23) language syntax compendium.
 * Build: $(CC) -std=c23 -Wall -Wextra -pedantic -Werror -pthread c23.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <uchar.h>
#include <complex.h>
#include <stdatomic.h>
#include <setjmp.h>
#include <signal.h>
#include <math.h>

/*
 * Section 1: Preprocessor Directives (ISO C23 Clause 6.10)
 */

#define STR_EXPAND(x) #x
#define STR(x) STR_EXPAND(x)
#define GLUE_TOKENS(a, b) a ## b
#define LOG_FMT(fmt, ...) printf(fmt __VA_OPT__(,) __VA_ARGS__)

#undef OMNI_UNDEFINED_FLAG
#define OMNI_ACTIVE_MACRO 1

#if __has_include(<stdio.h>)
#  if __has_c_attribute(nodiscard)
#    define HAS_NODISCARD_ATTR 1
#  endif
#elifdef OMNI_UNDEFINED_FLAG
#  error "Unreachable branch: elifdef"
#elifndef OMNI_ACTIVE_MACRO
#  error "Unreachable branch: elifndef"
#else
#  error "Unreachable branch: else"
#endif

#if 0
#warning "Standard C23 diagnostic warning directive"
#pragma STDC FP_CONTRACT ON
#endif

#if defined(__clang__)
#  pragma clang diagnostic push
#  pragma clang diagnostic ignored "-W#pragma-messages"
#endif
_Pragma("message(\"Omni: Verifying ISO C23 Language Construct Compliance\")")
#if defined(__clang__)
#  pragma clang diagnostic pop
#endif

/*
 * Section 2: Standard Attributes (Clause 6.7.12) and Assertions
 */

static_assert(__STDC_VERSION__ >= 202311L, "Must be ISO C23 or later");
static_assert(sizeof(int32_t) == 4);
static_assert(sizeof(int64_t) == 8, "int64_t must be 8 bytes");
_Static_assert(sizeof(char) == 1, "char is 1 byte by definition");

#if __has_c_attribute(reproducible)
#  define ATTR_REPRODUCIBLE [[reproducible]]
#else
#  define ATTR_REPRODUCIBLE
#endif

#if __has_c_attribute(unsequenced)
#  define ATTR_UNSEQUENCED [[unsequenced]]
#else
#  define ATTR_UNSEQUENCED
#endif

[[nodiscard("computation result must be consumed")]]
static inline int math_square(int x) ATTR_REPRODUCIBLE {
    return x * x;
}

static inline int math_increment(int x) ATTR_UNSEQUENCED {
    return x + 1;
}

[[deprecated("use modern_terminator instead")]]
[[maybe_unused]]
static void legacy_terminator(void) {
    exit(EXIT_FAILURE);
}

[[noreturn]]
static void modern_terminator(void) {
    unreachable();
}

/*
 * Section 3: Types, Enums, Bitfields, and Complex Declarators (Clause 6.7)
 */

typedef enum StateMachine : uint8_t {
    STATE_INIT = 0,
    STATE_WORK = 1,
    STATE_DONE = 2
} StateMachine;

typedef union RegisterWord {
    uint32_t raw;
    struct {
        uint32_t flag_a : 1;
        uint32_t flag_b : 1;
        uint32_t        : 2; /* Unnamed bitfield padding */
        uint32_t        : 0; /* Zero-width bitfield forces alignment to next boundary */
        uint32_t payload : 16;
    } bits;
} RegisterWord;

struct AlignedBlock {
    alignas(16) uint8_t simd_buffer[16];
    alignas(double) char aligned_as_double;
    _Alignas(16) uint8_t legacy_aligned[16];
};

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

typedef struct DynamicPacket {
    size_t length;
    int payload[]; /* Flexible array member */
} DynamicPacket;

/* Complex function and array pointer declarators */
static int static_array_data[3] = {100, 200, 300};

static int (*array_pointer_provider(void))[3] {
    return &static_array_data;
}

typedef int (*(*array_provider_fn)(void))[3];
typedef int (*binary_op_fn)(int, int);

static int op_multiply(int a, int b) { return a * b; }
static binary_op_fn dispatch_table[1] = { op_multiply };

/* Function prototype with variable length array dimension indicator [*] */
void matrix_worker(int rows, int cols, double matrix[*][*]);

void matrix_worker(int rows, int cols, double matrix[rows][cols]) {
    if (rows > 0 && cols > 0) matrix[0][0] = 42.0;
}

/* Parameter array qualified with static and restrict */
static void qualified_consumer(int buffer[static restrict 4]) {
    buffer[0] += 1;
}

/* Variadic function */
static int sum_variadic(size_t count, ...) {
    va_list ap;
    va_start(ap, count);
    int total = 0;
    for (size_t i = 0; i < count; i++) {
        total += va_arg(ap, int);
    }
    va_end(ap);
    return total;
}

/* C23 empty parameter list means (void) */
static int empty_param_worker() {
    return 7;
}

/* Generic type selection macro */
#define TYPE_NAME(x) _Generic((x), \
    bool: "bool", \
    char: "char", \
    signed char: "signed char", \
    unsigned char: "unsigned char", \
    short: "short", \
    unsigned short: "unsigned short", \
    int: "int", \
    unsigned int: "unsigned int", \
    long: "long", \
    unsigned long: "unsigned long", \
    long long: "long long", \
    unsigned long long: "unsigned long long", \
    float: "float", \
    double: "double", \
    long double: "long double", \
    nullptr_t: "nullptr_t", \
    default: "pointer/other")

/*
 * Section 4: Execution Context, Linkage, and Main Driver
 */

static jmp_buf nonlocal_buf;
extern int external_symbol;
int external_symbol = 0xAA;

static void sigusr_handler(int sig) {
    (void)sig;
}

int main(void) {
    /* Storage classes and type inference */
    auto deduced_double = 3.141592653589793;
    auto int legacy_auto = 1;
    register int fast_counter = 0;
    static unsigned long run_counter = 0;
    thread_local static int tls_var = 42;
    _Thread_local static int legacy_tls_var = 84;

    /* Constants, keywords, and type operators */
    constexpr int compile_magic = 0xBEEF;
    bool active_flag = true;
    active_flag = false;
    nullptr_t null_token = nullptr;
    int *null_ptr = nullptr;

    typeof(deduced_double) cloned_double = 2.71828;
    typeof_unqual(const volatile int) clean_integer = 128;

    /* Scalar types and literals */
    signed char s_char = -12;
    unsigned char u_char = 255U;
    short s_short = -32767;
    unsigned short u_short = 65535U;
    int s_int = -2147483647;
    unsigned int u_int = 4294967295U;
    long s_long = -2147483647L;
    unsigned long u_long = 4294967295UL;
    long long s_llong = -9'223'372'036'854'775'807LL;
    unsigned long long u_llong = 18'446'744'073'709'551'615ULL;

    /* Alignment operators */
    size_t align_c23 = alignof(struct AlignedBlock);
    size_t align_c11 = _Alignof(struct AlignedBlock);

    /* Digit separators, octal, binary, and hex floating point */
    int octal_literal = 0755;
    int binary_literal = 0b1010'1111'0000'0101;
    double hex_float = 0x1.0p-3;
    float dec_float = 1.25e-2f;
    long double ext_float = 1.0L;

    /* Universal character names in identifiers */
    int \u03c0_symbol = 314;

    /* Complex types */
    float complex complex_f = 1.0f + 2.0f * I;
    double _Complex complex_d = 3.0 + 4.0 * I;

    /* Character and string literals (standard, wide, unicode, UTF-8 char) */
    char c_ascii = 'A';
    wchar_t c_wide = L'Ω';
    char16_t c_u16 = u'ñ';
    char32_t c_u32 = U'Ψ';
    unsigned char c_u8 = u8'z';
    const char *s_ascii = "ASCII string";
    const wchar_t *s_wide = L"Wide string";
    const char16_t *s_u16 = u"UTF-16 string";
    const char32_t *s_u32 = U"UTF-32 string";
    const char8_t *s_u8 = u8"UTF-8 string";

    /* Exact-width integers */
#if defined(__BITINT_MAXWIDTH__)
    _BitInt(24) bit_int_val = -1234wb;
    unsigned _BitInt(48) u_bit_int_val = 0xABCD'EF01uwb;
#endif

    /* Qualifiers and atomic operations */
    const volatile int hw_reg = 0xCAFE;
    const volatile int *ptr_hw = &hw_reg;
    int memory_target = 10;
    int *const const_p = &memory_target;
    int *restrict restrict_p = &memory_target;

    _Atomic int atomic_counter = 0;
    _Atomic(uint32_t) atomic_wrapped = 100U;
    atomic_init(&atomic_counter, 1);
    atomic_fetch_add_explicit(&atomic_counter, 2, memory_order_relaxed);
    atomic_store_explicit(&atomic_wrapped, 200U, memory_order_release);
    atomic_flag atomic_spin = ATOMIC_FLAG_INIT;
    bool spin_acquired = !atomic_flag_test_and_set(&atomic_spin);
    if (spin_acquired) {
        atomic_flag_clear(&atomic_spin);
    }

    /* Universal zero-initializers, designated initializers, compound literals */
    int universal_zero_array[4] = {};
    struct Container empty_container = {};
    struct Container filled_container = {
        .id = 500,
        .sub_code = 12,
        .precision = 3.14159265
    };
    RegisterWord reg_word = {
        .bits = { .flag_a = 1, .flag_b = 0, .payload = 0x7FFF }
    };
    int sparse_indices[5] = { [0] = 1, [3] = 4 };

    int *compound_arr = (int[]){ 10, 20, 30 };
    struct Container compound_cont = (struct Container){ .id = 99, .sub_code = 1 };

    /* Block scope variable length array (VLA) */
    size_t dynamic_dim = (size_t)(fast_counter + 3);
    int vla_block[dynamic_dim];
    vla_block[0] = math_square(5);

    /* Dynamic allocation with flexible array member */
    DynamicPacket *packet = malloc(sizeof(DynamicPacket) + (sizeof(int) * 2));
    if (packet) {
        packet->length = 2;
        packet->payload[0] = 0x11;
        packet->payload[1] = 0x22;
        free(packet);
    }

    /* Embedded resource parameters */
#if defined(__has_embed)
#  if __has_embed("c23.c")
    static const unsigned char embedded_data[] = {
#    embed "c23.c" limit(4) prefix(0xAA, ) suffix(, 0xFF) if_empty(0x00)
    };
    int embed_checksum = embedded_data[0] + embedded_data[5];
#  else
    int embed_checksum = 0;
#  endif
#else
    int embed_checksum = 0;
#endif

    /* Operators, associativity, precedence chaining */
    int op_x = 20, op_y = 6;
    int arithmetic = ((op_x + op_y) * 2 - (op_x / op_y) + (op_x % op_y));
    int bitwise = ((op_x << 2) >> 1) ^ (~op_y & (op_x | 0x0F));
    bool logical = (op_x > op_y) && (op_x >= 20) && (op_y < 10) && (op_y <= 6) && (op_x != op_y);
    int ternary = logical ? (reg_word.bits.flag_a ? 100 : 200) : 300;
    int comma_res = (fast_counter++, fast_counter + 5);

    arithmetic += 1; arithmetic -= 1; arithmetic *= 2; arithmetic /= 2; arithmetic %= 100;
    bitwise &= 0xFF; bitwise ^= 0x0F; bitwise |= 0x10; bitwise <<= 1; bitwise >>= 1;

    /* Control flow and modern C23 label placement */
    StateMachine state = STATE_WORK;

    if (ternary == 100 && (state == STATE_WORK)) {
        goto label_pre_declaration;
    } else {
        while (false) {}
    }

label_pre_declaration:
    /* C23: Label placed directly before a declaration */
    int newly_declared_in_scope = 42;

    do {
        switch (state) {
            case STATE_INIT:
                run_counter++;
                [[fallthrough]];
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
                modern_terminator();
        }
    } while (0);

    {
        goto scoped_entry;
    scoped_entry:
        int scoped_num = 1;
        (void)scoped_num;
    [[maybe_unused]] label_block_terminal:
        /* C23: Label placed at the end of a block without trailing semicolon */
    }

    /* Non-local jumps, signals, floating-point environment */
    volatile bool jump_performed = false;
    if (setjmp(nonlocal_buf) == 0) {
        if (!jump_performed) {
            jump_performed = true;
            longjmp(nonlocal_buf, 1);
        }
    }
    signal(SIGUSR1, sigusr_handler);

    /* Calling function pointers, VLA prototypes, and qualifiers */
    array_provider_fn provider = array_pointer_provider;
    int (*resolved_triplet)[3] = provider();
    int triplet_element = (*resolved_triplet)[1];

    int dispatch_result = dispatch_table[0](10, 5);

    double test_matrix[2][2] = {};
    matrix_worker(2, 2, test_matrix);

    int test_seq[4] = {1, 2, 3, 4};
    qualified_consumer(test_seq);

    int variadic_sum = sum_variadic(3, 10, 20, 30);
    int empty_param_res = empty_param_worker();

    /* Predefined macros and token pasting */
    int GLUE_TOKENS(verified_, variable) = 999;
    const char *active_fn = __func__;

    LOG_FMT("File: %s | Line: %d | Func: %s | Token: %d\n",
            __FILE__, __LINE__, active_fn, verified_variable);

    printf("Omni C23 Verification: Type=%s | Square=%d | Incr=%d | Sum=%d | State=%u\n",
           TYPE_NAME(compile_magic), math_square(4), math_increment(9),
           variadic_sum, (unsigned)state);

    /*
     * Compact state hash: Consumes all declared scalars to guarantee
     * full compilation coverage without dead (void) suppressions.
     */
    long double checksum =
        (long double)legacy_auto + deduced_double + cloned_double + clean_integer +
        s_char + u_char + s_short + u_short + s_int + u_int + s_long + u_long +
        (s_llong + u_llong) + binary_literal + hex_float + dec_float + ext_float +
        creal(complex_f) + cimag(complex_d) + c_ascii + (int)c_wide + (int)c_u16 +
        (int)c_u32 + c_u8 + s_ascii[0] + s_wide[0] + s_u16[0] + s_u32[0] + s_u8[0] +
        *ptr_hw + *const_p + *restrict_p + atomic_counter + atomic_wrapped +
        universal_zero_array[0] + empty_container.id + filled_container.precision +
        reg_word.raw + sparse_indices[0] + compound_arr[0] + compound_cont.id +
        vla_block[0] + embed_checksum + arithmetic + bitwise + (int)logical +
        comma_res + newly_declared_in_scope + triplet_element + dispatch_result +
        test_matrix[0][0] + test_seq[0] + empty_param_res + run_counter +
        tls_var + legacy_tls_var + external_symbol + (null_token == null_ptr ? 1 : 0) +
        (active_flag ? 1 : 0) + (spin_acquired ? 1 : 0) +
        align_c23 + align_c11 + octal_literal + \u03c0_symbol;

#if defined(__BITINT_MAXWIDTH__)
    checksum += (long double)bit_int_val + (long double)u_bit_int_val;
#endif

    if (isnan((double)checksum)) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
