#if defined _WIN32

#include<windows.h>
#include<stdio.h>

DWORD WINAPI thread_func(LPVOID ignored) {
    printf("Printing from a thread.\n");
    return 0;
}

int main(int argc, char **argv) {
    DWORD id;
    HANDLE th;
    printf("Starting thread.\n");
    th = CreateThread(NULL, 0, thread_func, NULL, 0, &id);
    WaitForSingleObject(th, INFINITE);
    printf("Stopped thread.\n");
    return 0;
}
#else

#include<pthread.h>
#include<stdio.h>

void* main_func(void* ignored) {
    printf("Printing from a thread.\n");
    return NULL;
}

int main(int argc, char** argv) {
    pthread_t thread;
    int rc;
    printf("Starting thread.\n");
    rc = pthread_create(&thread, NULL, main_func, NULL);
    rc = pthread_join(thread, NULL);
    printf("Stopped thread.\n");
    return rc;
}

#endif
