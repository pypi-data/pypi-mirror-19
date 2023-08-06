#!/usr/bin/env python

from setuptools import setup

long_description = '''

'''

setup(
    name='ized',
    version='0.0.2',
    author='Ingo Fruend',
    author_email='ized@ingofruend.net',
    description='Spline expansions, multiple regularizers, '
    'and generalized linear models',
    license='MIT',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    packages=['ized'],
)
