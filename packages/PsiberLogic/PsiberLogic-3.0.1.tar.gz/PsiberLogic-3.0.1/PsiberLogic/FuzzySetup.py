# -*- coding: utf-8 -*-
try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
from Cython.Distutils import build_ext
import sys
import Cython.Compiler.Options
import os
import numpy as np
Cython.Compiler.Options.annotate = True

path = sys.exec_prefix+'\\Lib\\site-packages\\PsiberLogic'
os.chdir(path)
sys.argv.extend(['build_ext', '--inplace'])

setup(cmdclass={'build_ext': build_ext},
      ext_modules=[Extension("cPsiberLogic", ["cPsiberLogic.pyx"], extra_compile_args=['/O2'])],
      requires=['numpy', 'Cython'],
      include_dirs=[np.get_include()],
      )
