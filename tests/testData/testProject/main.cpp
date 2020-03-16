#ifdef PRINT_MESSAGE
  #define PRINT_MESSAGE_CONTENT #PRINT_MESSAGE
#else
  #define PRINT_MESSAGE_CONTENT ""
#endif 

#include <iostream>

int main() {
    std::cout << PRINT_MESSAGE_CONTENT << std::endl;
    return 0;
}