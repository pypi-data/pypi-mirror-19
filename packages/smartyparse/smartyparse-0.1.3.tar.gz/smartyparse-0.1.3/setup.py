''' Smartyparse: A python library for smart dynamic binary de/encoding.

Smartyparse! Intelligent general-purpose binary parsing, marshalling,
serializing, etc library. Capable of dynamic operations, self-describing
formats, nested formats, etc.
'''
import sys

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = (
    'Smartyparse is an intelligent general-purpose binary parsing, ' +
    'marshalling, serializing, etc library. Capable of dynamic operations, ' +
    'self-describing formats, nested formats, etc. Use it to encode, ' +
    'decode, and develop binary formats quickly and easily. It supports ' +
    '```python>=3.3```.'
)

# # If we're installing, don't bother building the long_description
# # Ewwww, this is dirty.
# if sys.argv[1] == 'sdist':
#     with open('README.md', 'r') as f:
#         s_readme = f.read()
        
#     # Get the long description from the README file
#     import pypandoc
#     long_description = pypandoc.convert(s_readme, 'rst', format='md')
#     with open('README.rst', 'w') as f:
#         f.write(long_description)

setup(
    name='smartyparse',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.3',

    description='A python library for smart dynamic binary de/encoding.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/Muterra/py_smartyparse',

    # Author details
    author='Muterra, Inc',
    author_email='badg@muterra.io',

    # Choose your license
    license='LGPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='smartyparse, data structure, dynamic, binary, parser, builder, pack, unpack',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
    },
)
