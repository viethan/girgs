from setuptools import setup, Extension
from Cython.Build import cythonize

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

ext_modules=[
	Extension('src.girg', ['src/girg.pyx'],),
	Extension('src.dnu', ['src/dnu.pyx'])
]

setup(
	ext_modules=cythonize(ext_modules, annotate=True)
)
