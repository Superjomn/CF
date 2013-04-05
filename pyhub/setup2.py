from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name = 'svdm',
    ext_modules=[
        Extension("svd",
            sources=["modelmain.pyx"], 
            include_dirs=["."],
            language="c++"),
    ],
    cmdclass = {'build_ext': build_ext},
)
