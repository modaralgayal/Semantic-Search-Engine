import pybind11
from setuptools import Extension, setup

ext_modules = [
    Extension(
        "cos_sim",
        ["bindable_functions/FlatIndex.cpp"],
        include_dirs=[
            pybind11.get_include(),
            "/usr/include/eigen3",
        ],
        language="c++",
    )
]


setup(name="cos_sim", version="0.1", ext_modules=ext_modules)
