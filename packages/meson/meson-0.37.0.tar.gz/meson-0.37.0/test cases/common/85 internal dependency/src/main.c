#include<stdio.h>
#include<proj1.h>

int main(int argc, char **argv) {
    printf("Now calling into library.\n");
    proj1_func1();
    proj1_func2();
    proj1_func3();
    return 0;
}
