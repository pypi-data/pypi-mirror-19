|mpnum|
=======

A matrix product representation library for Python
--------------------------------------------------

|Travis| |Documentation Status| |Coverage Status| |Code Climate| |PyPI|

This code is work in progress.

mpnum is a Python library providing flexible tools to implement new
numerical schemes based on matrix product states (MPS). So far, we
provide:

-  basic tools for various matrix product based representations, such
   as:
-  matrix product states
   (`MPS <http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-states-mps>`__),
   also known as tensor trains (TT)
-  matrix product operators
   (`MPO <http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-operators-mpo>`__)
-  local purification matrix product states
   (`PMPS <http://mpnum.readthedocs.org/en/latest/intro.html#local-purification-form-mps-pmps>`__)
-  arbitrary matrix product arrays
   (`MPA <http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-arrays>`__)
-  basic MPA operations: add, multiply, etc;
   `compression <http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.mparray.MPArray.compress>`__
   (SVD and variational)
-  computing `ground
   states <http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.linalg.mineig>`__
   (the smallest eigenvalue and eigenvector) of MPOs
-  flexible tools to implement new schemes based on matrix product
   representations

For more information, see:

-  `Introduction to
   mpnum <http://mpnum.readthedocs.org/en/latest/intro.html>`__
-  `Notebook with code examples <examples/mpnum_intro.ipynb>`__
-  `Library reference <http://mpnum.readthedocs.org/en/latest/>`__

Required packages:

-  six, numpy, scipy, sphinx (to build the documentation)

Supported Python versions:

-  2.7, 3.3, 3.4, 3.5

Contributors
------------

-  Daniel Suess, daniel@dsuess.me, `University of
   Cologne <http://www.thp.uni-koeln.de/gross/>`__
-  Milan Holzaepfel, mail@mjh.name, `Ulm
   University <http://qubit-ulm.com/>`__

License
-------

Distributed under the terms of the BSD 3-Clause License (see
`LICENSE <LICENSE>`__).

.. |mpnum| image:: docs/tensors_logo.png
.. |Travis| image:: https://travis-ci.org/dseuss/mpnum.svg?branch=master
   :target: https://travis-ci.org/dseuss/mpnum
.. |Documentation Status| image:: https://readthedocs.org/projects/mpnum/badge/?version=latest
   :target: http://mpnum.readthedocs.org/en/latest/?badge=latest
.. |Coverage Status| image:: https://coveralls.io/repos/github/dseuss/mpnum/badge.svg?branch=master
   :target: https://coveralls.io/github/dseuss/mpnum?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/dseuss/mpnum/badges/gpa.svg
   :target: https://codeclimate.com/github/dseuss/mpnum
.. |PyPI| image:: https://img.shields.io/pypi/v/mpnum.svg
   :target: https://pypi.python.org/pypi/mpnum/
