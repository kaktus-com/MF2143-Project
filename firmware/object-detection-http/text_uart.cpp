t#include <cstdio>
#include <unistd.h>

extern "C" void app_main(void*) {
  setvbuf(stdout, NULL, _IONBF, 0);

  while (true) {
    printf("{\"test\": 123}\n");
    fflush(stdout);
    usleep(20000);   // 20ms
  }
}
