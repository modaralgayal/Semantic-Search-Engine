import pybind11
from setuptools import Extension, setup

ext_modules = [
    Extension(
        "example",
        ["bindable_functions/example.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
    )
]


setup(name="example", version="0.1", ext_modules=ext_modules)
