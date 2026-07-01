#include <iostream>
#include <vector>
#include <chrono>
using namespace std;
using namespace chrono;

const char NL = '\n';

struct ColMajor3D {
    int depth, rows, cols;
    vector<int> data;

    ColMajor3D(int depth, int rows, int cols)
        : depth(depth), rows(rows), cols(cols), data(depth * rows * cols) {}

    int& at(int d, int r, int c) {
        return data[r + c * rows + d * (rows * cols)];
    }

    int& pt(int d, int r, int c) {
        return data[c + r * cols + d * (rows * cols)];
    }

    void fill_c() {
        int val = 1;
        for (int d = 0; d < depth; d++)
            for (int c = 0; c < cols; c++)
                for (int r = 0; r < rows; r++)
                    at(d, r, c) = val++;
    }

    void fill_r() {
        int val = 1;
        for (int d = 0; d < depth; d++)
            for (int c = 0; c < cols; c++)
                for (int r = 0; r < rows; r++)
                    pt(d, r, c) = val++;
    }
};

int main() {
    ColMajor3D mat(100, 300, 400);
    mat.fill_c();

    long long sum = 0;
    auto st = high_resolution_clock::now();
    for (int d = 0; d < mat.depth; d++)
        for (int c = 0; c < mat.cols; c++)
            for (int r = 0; r < mat.rows; r++)
                sum += mat.at(d, r, c);
    auto p = high_resolution_clock::now();
    cout << "Col-major traversal | sum: " << sum << " | time: "
         << duration_cast<microseconds>(p - st).count() << "us" << NL;

    ColMajor3D pat(100, 300, 400);
    pat.fill_r();
    
    sum = 0;
    st = high_resolution_clock::now();
    for (int d = 0; d < pat.depth; d++)
        for (int r = 0; r < pat.rows; r++)
            for (int c = 0; c < pat.cols; c++)
                sum += pat.pt(d, r, c);
    p = high_resolution_clock::now();
    cout << "Row-major traversal | sum: " << sum << " | time: "
         << duration_cast<microseconds>(p - st).count() << "us" << NL;

    return 0; 
}

// Col-major traversal | sum: 72000006000000 | time: 71028us
// Row-major traversal | sum: 72000006000000 | time: 49558us

// Assignemnt, do the same thing with a 2D Array. 