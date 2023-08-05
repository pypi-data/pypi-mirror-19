#include<stdlib.h>
#if defined _WIN32 || defined __CYGWIN__
#define DLL_PUBLIC __declspec(dllexport)
#else
  #if defined __GNUC__
    #define DLL_PUBLIC __attribute__ ((visibility("default")))
  #else
    #pragma message ("Compiler does not support symbol visibility.")
    #define DLL_PUBLIC
  #endif
#endif


char func_c();

char DLL_PUBLIC func_b() {
    if(func_c() != 'c') {
        exit(3);
    }
    return 'b';
}
