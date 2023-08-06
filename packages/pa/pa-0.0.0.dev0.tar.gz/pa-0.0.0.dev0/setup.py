#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pa',
    version='0.0.0.dev',
    description='Paper Arxiv: A command line based academic paper management tool.',
    url='',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    keywords='paper arxiv manage',
    install_requires=[
          'click',
    ],
    entry_points={
          'console_scripts': [
              'pa = paper_arxiv.paper_arxiv:main'
          ]
    },
)
