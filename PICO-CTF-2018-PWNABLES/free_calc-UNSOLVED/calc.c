#define _XOPEN_SOURCE 700
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

#define FMAX 16

enum optype {CONSTANT, ADD, MULTIPLY, SUBTRACT, DIVIDE, NOOP, FUNCTION, FUNCDEF, EQUALS};

struct operation;

typedef struct funcdef {
    char *name;
    struct operation *ops;
    size_t opcount;
} funcdef_t;

typedef union opval {
    long ival;
    funcdef_t *fval;
} opval_t;

typedef struct operation {
    long t;
    opval_t v;
} operation_t;

typedef struct stack_el {
    long val;
    struct stack_el *next;
} stack_el_t;

typedef stack_el_t* stack_t;

bool parse_op(char*, operation_t*);

funcdef_t *functions[FMAX];
size_t fid = 0;


// Memory
void *xmalloc(size_t size) {
    void *ptr = malloc(size);
    if (ptr == NULL) {
        puts("malloc failed.");
        exit(1);
    }
    return ptr;
}

void *xrealloc(void *ptr, size_t size) {
    void *rptr = realloc(ptr, size);
    if (rptr == NULL) {
        puts("realloc failed.");
        exit(1);
    }
    return rptr;
}

// Stack
void push(stack_t *s, long v) {
    stack_el_t *el = xmalloc(sizeof(stack_el_t));

    el->val = v;
    el->next = *s;

    *s = el;
}

long pop(stack_t *s) {
    if (*s == NULL) {
        puts("Attempted to pop empty stack.");
        exit(1);
    }

    stack_el_t *el = *s;
    *s = el->next;
    long val = el->val;
    free(el);

    return val;
}

void define_function(funcdef_t *f) {
    for (size_t i = 0; i < fid; i++) {
        if (!strcmp(functions[i]->name, f->name)) {
            // Function already exists.
            funcdef_t *oldf = functions[i];
            if (f->opcount > oldf->opcount) {
                // Resize ops array
                oldf->ops = xrealloc(oldf->ops, f->opcount * sizeof(operation_t));
                oldf->opcount = f->opcount;
            }
            // Copy new ops to old ops
            memcpy(oldf->ops, f->ops, f->opcount * sizeof(operation_t));

            free(f->ops);
            free(f->name);
            free(f);

            return;
        }
    }

    // Function has not been defined.
    if (fid >= FMAX) {
        puts("Too many functions defined.");
        exit(1);
    }
    
    functions[fid++] = f; 
}

funcdef_t *read_function() {
    char *fname = strtok(NULL, " ");
    if (fname == NULL) {
        puts("Invalid function name.");
        exit(1);
    }
    char *fargs = strtok(NULL, " ");
    if (fargs == NULL) {
        puts("Invalid argument count.");
        exit(1);
    }

    size_t farg;
    int fnread = sscanf(fargs, "%zu", &farg);
    if (fnread != 1) {
        puts("Invalid argument count.");
        exit(1);
    }

    funcdef_t *f = NULL;

    f = xmalloc(sizeof(funcdef_t));
    f->name = xmalloc((strlen(fname) + 1) * sizeof(char));
    strcpy(f->name, fname);
    f->ops = xmalloc(farg * sizeof(operation_t));
    f->opcount = farg;

    for (size_t i = 0; i < farg; i++) {
        bool res = false;

        while (!res) {
            // Read until we find a valid operation.
            char *op_string = strtok(NULL, " ");
            if (op_string == NULL) {
                puts("Not enough function arguments.");
                exit(1);
            }
            res = parse_op(op_string, f->ops + i);
        }
    }

    return f;
}

bool parse_op(char *op_string, operation_t *op) {
    long constant;
    long n = sscanf(op_string, "%ld", &constant);
    if (n == 1) {
        // This is an integer
        op->t = CONSTANT;
        op->v.ival = constant;
    }
    else if (!strcmp(op_string, "+")) {
        op->t = ADD;
    }
    else if (!strcmp(op_string, "*")) {
        op->t = MULTIPLY;
    }
    else if (!strcmp(op_string, "-")) {
        op->t = SUBTRACT;
    }
    else if (!strcmp(op_string, "/")) {
        op->t = DIVIDE;
    }
    else if (!strcmp(op_string, "=")) {
        op->t = EQUALS;
    }
    else if (!strcmp(op_string, "#")) {
        op->t = NOOP;
    }
    else if (!strcmp(op_string, ":")) {
        op->t = FUNCDEF;
        op->v.fval = read_function();
    }
    else {
        for (size_t i = 0; i < fid; i++) {
            if (!strcmp(functions[i]->name, op_string)) {
                // Matches a function definition

                op->t = FUNCTION;
                op->v.fval = functions[i];
                return true;
            }
        }

        printf("Invalid operation '%s'\n", op_string);
        return false;
    }
    return true;
}

void run_op(operation_t *op, stack_t *s) {
    funcdef_t *f;
    size_t i;
    long s1, s2;

    switch (op->t) {
        case CONSTANT:
            push(s, op->v.ival);
            break;
        case FUNCTION:
            f = op->v.fval;
            printf("Running %s\n", f->name);
            
            for (i = 0; i < f->opcount; i++) {
                run_op(f->ops + i, s);
            }

            break;
        case ADD:
            s2 = pop(s);
            s1 = pop(s);
            push(s, s1 + s2);
            break;
        case MULTIPLY:
            s2 = pop(s);
            s1 = pop(s);
            push(s, s1 * s2);
            break;
        case SUBTRACT:
            s2 = pop(s);
            s1 = pop(s);
            push(s, s1 - s2);
            break;
        case DIVIDE:
            s2 = pop(s);
            s1 = pop(s);
            push(s, s1 / s2);
            break;
        case EQUALS:
            s1 = pop(s);
            printf("%ld\n", s1);
            break;
        case FUNCDEF:
            define_function(op->v.fval);
            break;
        case NOOP:
            break;
        default:
            printf("Invalid operation '%ld'\n", op->t);
            break;
    }
}

int main() {

  setvbuf(stdout, NULL, _IONBF, 0);
  
    char *line = NULL;
    size_t n = 0;
    stack_t s = NULL;

    setbuf(stdin, NULL);

    puts("Welcome to heapcalc!");
    puts("This is a postfix calculator. Commands: + * - / = # constant function");
    puts(" Example: '1 1 + =' outputs 2.");
    puts("Define functions like ': <name> <opcount> <op1> <op2> ...'");
    puts(" Example: ': add 1 +' defines a function add with one operation which executes '+'.");
    puts("Good luck!");

 
    while (true) {
        printf(">> ");
        ssize_t nread = getline(&line, &n, stdin);
        if (nread == -1) return 1;
        if (line[nread - 1] == '\n') line[nread - 1] = '\0';

        char *op_string = strtok(line, " ");

        while (op_string != NULL) {
            operation_t op;
            bool res = parse_op(op_string, &op);

            if (res) run_op(&op, &s);

            op_string = strtok(NULL, " ");
        }
	
        free(line);
    }
    return 0;
}
