from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
      name = 'PsiberLogic',
      packages = ['PsiberLogic','PsiberLogic.demo'], # this must be the same as the name above
      version = '3.0.1',
      description = 'A speed-optimized, barebones, Python 3 fuzzy controller package.',
      long_description=long_description,
      author = 'Psibernetix Inc.',
      author_email = 'contact@psibernetix.com',
      keywords = 'Fuzzy Logic',
      license = 'GNU Library or Lesser General Public License (LGPL)',
      url = "http://packages.python.org/psiberlogic",
      install_requires = ['numpy', 'cython'],
      package_data = {'': ['*.pyx', '*.py', '*.txt']},
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                     'Programming Language :: Python :: 3',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Education',
                     'Intended Audience :: Science/Research',
                     'Topic :: Scientific/Engineering',
                     ],
)