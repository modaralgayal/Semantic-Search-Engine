#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip> 
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


using namespace std;
const string NL = "\n";

struct SearchResults {
    vector<int> ids;
    vector<double> scores;
};


class FlatIndex {
    public: 
        FlatIndex(size_t dimension, size_t library) 
            : dim(dimension), lib(library), count(0) 
        {
            embeddings = new float*[lib];
            embeddings[0] = new float[lib * dim];

            for (size_t i = 1; i < lib; i++) {
                embeddings[i] = embeddings[i-1] + dim;
            }
        }

        ~FlatIndex() {
            delete[] embeddings[0]; // free the single flat allocation
            delete[] embeddings;    // free the array of row-pointers
        }

        void add(const vector<float>& embedding, int id) {
            if (embedding.size() != dim) {
                throw runtime_error("Embedding dimension mismatch");
            }
            if (count >= lib) {
                throw runtime_error("Index is full");
            }
            double norm_sq = 0.0; 
            for (size_t i = 0; i < dim; i++) norm_sq += embedding[i] * embedding[i];
            norms.push_back(sqrt(norm_sq)); 
            copy(embedding.begin(), embedding.end(), embeddings[count]);
            IDs.push_back(id);
            count++; 
        };

        SearchResults search(vector<float>& query, size_t k) { 
        vector<pair<double, int>> sorted_scores;
        double score = 0.0; 

        double query_norm = 0.0;
        for (size_t i = 0; i < dim; i++) query_norm += query[i] * query[i];

        for (size_t i = 0; i < lib; i++) {
            float* row_i = embeddings[i];
            score = similarity(query.data(), row_i, i, sqrt(query_norm));
            sorted_scores.push_back({score, IDs[i]});
        }

        // We sort ascending by score
        partial_sort(sorted_scores.begin(), sorted_scores.begin() + k, sorted_scores.end(),
        [](const pair<double,int>& a, pair<double,int>& b) {
            return a.first > b.first;
        });

        SearchResults results; 
        for (size_t i = 0; i < k && i < sorted_scores.size(); i++) {
            results.scores.push_back(sorted_scores[i].first);
            results.ids.push_back(sorted_scores[i].second);
        }

        return results; 
    };   

    private:
        size_t dim;
        size_t lib;
        size_t count;
        vector<double> norms; 
        float** embeddings;
     

        vector<int> IDs;
            // calculate using cosine similarity
    double similarity(const float* query, const float* embedding_vector, size_t i, double query_norm) {
        // n is the dim
        double dot = 0.0;
        for (size_t j = 0; j < dim; j++) {
            dot += query[j] * embedding_vector[j];
        }
        return dot / (query_norm * norms[i]);

    }};


namespace py = pybind11;

PYBIND11_MODULE(cos_sim, m) {
    py::class_<FlatIndex>(m, "FlatIndex")
        .def(py::init<size_t, size_t>())
        .def("add", &FlatIndex::add)
        .def("search", &FlatIndex::search);
    py::class_<SearchResults>(m, "SearchResults")
        .def_readonly("ids", &SearchResults::ids)
        .def_readonly("scores", &SearchResults::scores);
}
