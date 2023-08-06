# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from setuptools import setup, find_packages


def main():
    CLASSIFIERS = """\
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
Topic :: Utilities
""".splitlines()

    setup(
        name='gevent-tools',
        version='0.1.1',
        packages=find_packages(),
        install_requires=[
            'six>=1.10',
            'gevent>=1.0',
            'treelib>=1.0'],
        license='MIT',
        classifiers=CLASSIFIERS,
        author='Tiago Coutinho',
        author_email='coutinhotiago@gmail.com',
        description='gevent utilities library',
        long_description=open('README.md').read(),
        url='https://github.com/tiagocoutinho/gtools',
        download_url='http://pypi.python.org/pypi/gevent-tools',
        platforms=['Linux', 'Windows XP/Vista/7/8/10'],
        keywords=['gevent', 'tools'],
        )

if __name__ == '__main__':
    main()
