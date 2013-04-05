from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(
   ["modelmain.pyx"],                 # our Cython source
   sources=['../common.cpp', '../Data.cpp', '../models/svd.cpp'],
   language="c++",             # generate C++ code
))
