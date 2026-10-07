/*
 * omni: c89.c
 * Canonical, exhaustive ANSI X3.159-1989 / ISO/IEC 9899:1990 (C89/C90) language compendium.
 * Build: $(CC) -std=c89 -Wall -Wextra -pedantic -Werror c89.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <limits.h>
#include <float.h>
#include <stdarg.h>
#include <setjmp.h>
#include <signal.h>
#include <math.h>

/*
 * Section 1: Preprocessor Directives (C89 Clause 3.8 / ISO 6.8)
 */

#define STR_EXPAND(x) #x
#define STR(x) STR_EXPAND(x)
#define GLUE(a, b) a ## b
#define SQR(x) ((x) * (x))

#undef OMNI_UNDEFINED
#define OMNI_C89_ACTIVE 1

#ifndef __STDC__
#  error "Strict ANSI C conformance required"
#endif

#ifdef __STDC_VERSION__
#  error "__STDC_VERSION__ is not defined in ANSI C89 / ISO C90"
#endif

#if defined(OMNI_C89_ACTIVE)
#  define CONFIG_FLAG 1
#elif !defined(OMNI_UNDEFINED)
#  error "Unreachable branch"
#else
#  error "Unreachable branch"
#endif

#pragma pack()

/*
 * Section 2: Types, Declarators, Structs, Unions, Enums (C89 Clause 3.5 / ISO 6.5)
 */

enum Status {
    STATUS_INIT = 0,
    STATUS_WORK = 1,
    STATUS_DONE = 2
    /* Note: Trailing comma is forbidden in C89 */
};

struct BitFieldUnit {
    unsigned int flag_a : 1;
    unsigned int flag_b : 1;
    unsigned int        : 2; /* Unnamed padding bitfield */
    unsigned int        : 0; /* Force alignment to next storage boundary */
    unsigned int val    : 4;
};

union DataPayload {
    int id;
    float alt_id;
    char raw[sizeof(float)];
};

struct Record {
    struct BitFieldUnit flags;
    union DataPayload payload;
    double precision;
};

/* Pointer to array and complex function pointer types */
static int backing_array[3] = {10, 20, 30};

static int (*array_provider(void))[3] {
    return &backing_array;
}

typedef int (*(*array_provider_fn)(void))[3];
typedef int (*binary_op_fn)(int, int);

static int op_multiply(int a, int b) {
    return a * b;
}

static binary_op_fn dispatch_table[1] = { op_multiply };

/* Variadic function conforming to C89 stdarg.h */
static int sum_variadic(int count, ...) {
    va_list ap;
    int total = 0;
    int i;

    va_start(ap, count);
    for (i = 0; i < count; i++) {
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
    volatile int jump_performed;
    jump_performed = 0;
    if (setjmp(nonlocal_buf) == 0) {
        if (!jump_performed) {
            jump_performed = 1;
            longjmp(nonlocal_buf, 1);
        }
    }
    return jump_performed;
}

int main(void) {
    /*
     * In C89, all declarations within any block MUST strictly precede
     * all statements. Mixing declarations and code is forbidden.
     */
    auto int legacy_auto;
    register int fast_counter;
    static unsigned long run_counter;

    const volatile int hw_reg = 0xBEEF;
    const volatile int *ptr_hw;
    int memory_target;
    int *const const_p = &memory_target;

    signed char s_char;
    unsigned char u_char;
    short s_short;
    unsigned short u_short;
    int s_int;
    unsigned int u_int;
    long s_long;
    unsigned long u_long;

    float dec_float;
    double reg_double;
    long double ext_double;

    int octal_literal;
    int hex_literal;

    char c_ascii;
    wchar_t c_wide;
    const char *s_ascii;
    const wchar_t *s_wide;

    enum Status current_status;
    struct Record record_inst;
    int static_arr[4];

    int GLUE(symbolic_, var);
    int op_x, op_y;
    int arithmetic, bitwise;
    int logical, ternary, comma_res;

    int jump_result;
    array_provider_fn provider;
    int (*resolved_triplet)[3];
    int triplet_val;
    int dispatch_res;
    int var_sum;
    int i;
    double checksum;

    /* Statements start strictly here */
    legacy_auto = 1;
    fast_counter = 0;
    run_counter = 0;

    memory_target = 10;
    ptr_hw = &hw_reg;

    s_char = -12;
    u_char = 255U;
    s_short = -32767;
    u_short = 65535U;
    s_int = -32767;
    u_int = 65535U;
    s_long = -2147483647L;
    u_long = 4294967295UL;

    dec_float = 1.25e-2f;
    reg_double = 3.1415926535;
    ext_double = 2.718281828L;

    octal_literal = 0755;
    hex_literal = 0xABCD;

    c_ascii = 'A';
    c_wide = L'Z';
    s_ascii = "ANSI C89" " Literal Concatenation";
    s_wide = L"Wide String";

    current_status = STATUS_WORK;

    record_inst.flags.flag_a = 1;
    record_inst.flags.flag_b = 0;
    record_inst.flags.val = 7;
    record_inst.payload.id = 500;
    record_inst.precision = 0.001;

    static_arr[0] = 1;
    static_arr[1] = 2;
    static_arr[2] = 3;
    static_arr[3] = 4;

    symbolic_var = 123;

    op_x = 20;
    op_y = 6;
    arithmetic = ((op_x + op_y) * 2 - (op_x / op_y) + (op_x % op_y));
    bitwise = ((op_x << 2) >> 1) ^ (~op_y & (op_x | 0x0F));
    logical = (op_x > op_y) && (op_x >= 20) && (op_y < 10) && (op_y <= 6) && (op_x != op_y);
    ternary = logical ? (record_inst.flags.flag_a ? 100 : 200) : 300;
    comma_res = (fast_counter++, fast_counter + 5);

    arithmetic += 1; arithmetic -= 1; arithmetic *= 2; arithmetic /= 2; arithmetic %= 100;
    bitwise &= 0xFF; bitwise ^= 0x0F; bitwise |= 0x10; bitwise <<= 1; bitwise >>= 1;

    if (ternary == 100 && current_status == STATUS_WORK) {
        goto target_label;
    } else {
        while (0) {
            /* Empty loop */
        }
    }

target_label:
    do {
        switch (current_status) {
            case STATUS_INIT:
                run_counter++;
                /* Fallthrough */
            case STATUS_WORK:
                for (i = 0; i < 3; i++) {
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

    if (ternary == 999) {
        goto end_control_label;
    }

    /* In C89, labels require an explicit statement (e.g. null statement ;) */
end_control_label: ;

    jump_result = execute_nonlocal_jump();
    signal(SIGUSR1, sigusr_handler);

    provider = array_provider;
    resolved_triplet = provider();
    triplet_val = (*resolved_triplet)[1];

    dispatch_res = dispatch_table[0](10, 5);
    var_sum = sum_variadic(3, 10, 20, 30);

    printf("File: %s | Line: %d | Symbol: %d\n", __FILE__, __LINE__, symbolic_var);
    printf("C89 check: Sqr=%d | Sum=%d | Triplet=%d | Dispatch=%d | Runs=%lu\n",
           SQR(5), var_sum, triplet_val, dispatch_res, run_counter);

    checksum =
        (double)legacy_auto + fast_counter + run_counter + *ptr_hw + *const_p +
        s_char + u_char + s_short + u_short + s_int + u_int + s_long + u_long +
        dec_float + reg_double + (double)ext_double + octal_literal + hex_literal +
        c_ascii + (int)c_wide + s_ascii[0] + (int)s_wide[0] + current_status +
        record_inst.flags.val + record_inst.payload.id + record_inst.precision +
        static_arr[0] + symbolic_var + arithmetic + bitwise + logical + ternary +
        comma_res + triplet_val + dispatch_res + var_sum + external_symbol +
        CONFIG_FLAG + jump_result;

    if (checksum < 0.0) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
