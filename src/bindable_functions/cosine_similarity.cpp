#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>

using namespace std;
const string NL = "\n";

double dotProduct(vector<float>& vec1, vector<float>& vec2) {
    return inner_product(vec1.begin(), vec1.end(), vec2.begin(), 0.0);
}

double cosine_similarity(vector<float>& vec1, vector<float>& vec2) {
    double dot = dotProduct(vec1, vec2);
    double length = sqrt(dotProduct(vec1, vec1)) * sqrt(dotProduct(vec2, vec2));

    // cout << length << NL;

    return dot / length; 
}

int main() {
    vector<float> v1 = {1.0, 5.0, 6.7};
    vector<float> v2 = {1.0, 23, 477};

    cout << cosine_similarity(v1, v2) << NL;
}