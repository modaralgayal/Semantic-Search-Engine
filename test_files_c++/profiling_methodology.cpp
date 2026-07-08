#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

void fastFunction () {
    double result = 0.0;
    for (int i = 0; i <= 1000000; i++) {
        result += sin(i) * cos(i);
    }
}

void slowFunction() {
    double result = 0.0;
    for (int i = 1; i <= 3*1000000; ++i) {
        result += sqrt(i) * log(i);
    }
}

int main() {
    cout << "Profiling Example Program \n";

    for (int i = 0; i < 5; i++) {
        fastFunction();
        slowFunction();
    }
    cout << "Program Completed. \n";
    return 0; 
}
