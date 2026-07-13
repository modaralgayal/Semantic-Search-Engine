#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip> 

using namespace std;
const string NL = "\n";

struct SearchResults {
    vector<int> ids;
    vector<double> scores;
};


class FlatIndex {
    public: 
        FlatIndex(size_t dimension) : dim(dimension) {};

        void add(const vector<float>& embedding, int id) {
            if (embedding.size() != dim) {
                throw runtime_error("Embedding dimension mismatch");
            }
            embeddings.push_back(embedding);
            IDs.push_back(id);
        };

        SearchResults search(vector<float>& query, size_t k) { 
        vector<pair<double, int>> scores;
        double score = 0.0; 

        for (int i = 0; i < embeddings.size(); i++) {
            score = similarity(query, embeddings[i]);
            scores.push_back({score, IDs[i]});
        }

        // We sort ascending by score
        sort(scores.begin(), scores.end(),
        [](const pair<double,int>& a, pair<double,int>& b) {
            return a.first > b.first;
        });

        SearchResults results; 
        for (size_t i = 0; i < k && i < scores.size(); i++) {
            results.scores.push_back(scores[i].first);
            results.ids.push_back(scores[i].second);
        }

        return results; 
    };   

    private:
        size_t dim;
        vector<vector<float>> embeddings;
        vector<int> IDs;
            // calculate using cosine similarity
    double similarity(vector<float>& query, vector<float>& embedding_vector) {
        int n = query.size();
        double dot = 0.0, denom_a = 0.0, denom_b = 0.0; 
        for (int i = 0; i < n; i++) {
            dot += query[i] * embedding_vector[i];
            denom_a += query[i] * query[i];
            denom_b += embedding_vector[i] * embedding_vector[i];
        }

        return dot / (sqrt(denom_a) * sqrt(denom_b));
    }};

    

int main () {
    vector<vector<float>> embeddings = {
    {1.0, 0.0, 0.0}, 
    {5.0, 0.0, 0.0}, 
    {-1.0, 6.0, 0.0}, 
    {-15.0, 0.0, 0.0}};

    vector<float> query = {1.0,0.0,0.0};

    const size_t dim = 3; 
    FlatIndex index(dim);

    for (size_t i = 0; i < embeddings.size(); i++) {
        index.add(embeddings[i], i);
    }

    SearchResults results = index.search(query, 4);


    cout << "Query: [1, 0, 0]\n";
    cout << "Rank  ID  Score\n";

    for (size_t i = 0; i < results.ids.size(); i++) {
        cout << (i + 1) << "     " << results.ids[i] << "   " << results.scores[i] << "\n";
    }

    return 0; 
}
