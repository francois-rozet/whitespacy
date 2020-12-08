#include <stdio.h>

#define NICE 69420

int isNice(int x) {
    return x == NICE;
}

/* tricky quote " */
#define min(x, y) \
((x) < (y) ? (x) : (y))

int main() {
    printf("Hello, World!\n");

    if (isNice(3 * 4 * 5 * min(13, 31) * 89))
        printf("nice.\n");

    /* tricky //
       string */
    if (0)
        printf("/* */ \" // \
        ");

    return 0; // no error
}
