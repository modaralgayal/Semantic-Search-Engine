import pybind11
from setuptools import Extension, setup

ext_modules = [
    Extension(
        "cosine_similarity",
        ["bindable_functions/cosine_similarity.cpp"],
        include_dirs=[
            pybind11.get_include(),
            "/usr/include/eigen3",
        ],
        language="c++",
    )
]


setup(name="cosine_similarity", version="0.1", ext_modules=ext_modules)
