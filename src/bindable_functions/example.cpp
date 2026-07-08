#include <iostream>
#include <pybind11/pybind11.h>

using namespace std; 


int add(int a, int b) {
    return a + b; 
}

int subtract(int a, int b) {
    return a - b; 
}

namespace py = pybind11;

PYBIND11_MODULE(example, m, py::mod_gil_not_used()) {
    m.doc() = "pybind11 example module"; // Module docstring (optional)
    m.def("add", &add, "A function that add two numbers");
}
