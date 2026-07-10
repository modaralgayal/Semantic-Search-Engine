#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>
#include <Eigen/Dense>

using namespace std;
namespace py = pybind11;
using Eigen::MatrixXd;
const string NL = "\n";

MatrixXd normalize_embeddings(const MatrixXd& mat) {
    MatrixXd result = mat; 
    for (int i = 0; i < mat.rows(); i++) {
        double normalized = mat.row(i).norm();
        if (normalized > 0.0) {
            result.row(i) /= normalized; 
        }
    }
    return result;
}

MatrixXd cosine_similarity(const MatrixXd& a, const MatrixXd& b) {
    MatrixXd a_norm = normalize_embeddings(a);
    MatrixXd b_norm = normalize_embeddings(b);
    return a_norm * b_norm.transpose();

}

PYBIND11_MODULE(cosine_similarity, m, py::mod_gil_not_used()) {
    m.doc() = "Cosine fimilarity function";
    m.def("cosine_similarity", &cosine_similarity, 
        "A function the returns the cosine similarity between to vectors."
    );
}