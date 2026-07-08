#include <iostream>
#include <chrono>
#include <vector>

using namespace std; 
using namespace std::chrono;
const string NL = "\n";


struct Major2D {
    int rows, cols;
    vector<int> data;

    Major2D (int rows, int cols)
        :rows(rows), cols(cols), data(rows * cols) {};


    int& ac_c(int i, int j) {
        return data[i*cols + j];
    }

    int& ac_f(int i, int j) {
        return data[j*rows + i];
    }

    // Build function
    void fill_c() {
        int val = 1;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                ac_c(i,j) = val++; 
            }
        }
    }

    void fill_f() {
        int val = 1;
        for (int j = 0; j < cols; j++) {
            for (int i = 0; i < rows; i++) {
                ac_f(i,j) = val++; 
            }
        }
    }
};

int main() {
    Major2D mat(100,20);
    mat.fill_c();


    auto start = high_resolution_clock::now();
    int sum = 0; 
    for (int i = 0; i < mat.rows; i++) {
        for (int j = 0; j < mat.cols; j++) {
            sum += mat.ac_c(i, j);
        }
    }
    auto stop = high_resolution_clock::now();
    auto duration_1 = duration_cast<microseconds>(stop-start).count();

    start = high_resolution_clock::now();
    Major2D pat(100,20);
    pat.fill_f();
    sum = 0; 
    for (int i = 0; i < pat.rows; i++) {
        for (int j = 0; j < pat.cols; j++) {
            sum += pat.ac_f(i, j);
        }
    }
    stop = high_resolution_clock::now();
    auto duration_2 = duration_cast<microseconds>(stop-start).count();


    cout << "C order time: " << duration_1 << " ms" << NL;
    cout << "Fortran order time: " << duration_2 << " ms" << NL;
    // C order time: 6 ms
    // Fortran order time: 22 ms
    return 0; 
}

