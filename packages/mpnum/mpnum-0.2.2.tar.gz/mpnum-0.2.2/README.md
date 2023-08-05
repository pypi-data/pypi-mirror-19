![mpnum](docs/tensors_logo.png)
=====


## A matrix product representation library for Python

[![Travis](https://travis-ci.org/dseuss/mpnum.svg?branch=master)](https://travis-ci.org/dseuss/mpnum)
[![Documentation Status](https://readthedocs.org/projects/mpnum/badge/?version=latest)](http://mpnum.readthedocs.org/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/dseuss/mpnum/badge.svg?branch=master)](https://coveralls.io/github/dseuss/mpnum?branch=master)
[![Code Climate](https://codeclimate.com/github/dseuss/mpnum/badges/gpa.svg)](https://codeclimate.com/github/dseuss/mpnum)
[![PyPI](https://img.shields.io/pypi/v/mpnum.svg)](https://pypi.python.org/pypi/mpnum/)

This code is work in progress.

mpnum is a Python library providing flexible tools to implement new numerical schemes based on matrix product states (MPS). So far, we provide:

* basic tools for various matrix product based representations, such as:
 * matrix product states ([MPS](http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-states-mps)), also known as tensor trains (TT)
 * matrix product operators ([MPO](http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-operators-mpo))
 * local purification matrix product states ([PMPS](http://mpnum.readthedocs.org/en/latest/intro.html#local-purification-form-mps-pmps))
 * arbitrary matrix product arrays ([MPA](http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-arrays))
* basic MPA operations: add, multiply, etc; [compression](http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.mparray.MPArray.compress) (SVD and variational)
* computing [ground states](http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.linalg.mineig) (the smallest eigenvalue and eigenvector) of MPOs
* flexible tools to implement new schemes based on matrix product representations

For more information, see:

* [Introduction to mpnum](http://mpnum.readthedocs.org/en/latest/intro.html)
* [Notebook with code examples](examples/mpnum_intro.ipynb)
* [Library reference](http://mpnum.readthedocs.org/en/latest/)

Required packages:

* six, numpy, scipy, sphinx (to build the documentation)

Supported Python versions:

* 2.7, 3.3, 3.4, 3.5


## Contributors

* Daniel Suess, <daniel@dsuess.me>, [University of Cologne](http://www.thp.uni-koeln.de/gross/)
* Milan Holzaepfel, <mail@mjh.name>, [Ulm University](http://qubit-ulm.com/)


## License

Distributed under the terms of the BSD 3-Clause License (see [LICENSE](LICENSE)).
