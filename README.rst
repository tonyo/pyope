pyope
=====

|PyPi version|

This is an implementation of Boldyreva symmetric `order-preserving encryption`_ scheme (`Boldyreva's paper`_).

Quick example
-------------

::

  from pyope.ope import OPE
  cipher = OPE(b'key goes here')
  assert cipher.encrypt(1000) < cipher.encrypt(2000) < cipher.encrypt(3000)
  assert cipher.decrypt(cipher.encrypt(1337)) == 1337


Running tests
-------------

::

$ py.test tests/

TODO
----

- More tests
- Get rid of numpy dependency (rewrite hypergeometric sampling code?)
- Optimize speed
- Security guarantees


.. |PyPi version| image:: https://pypip.in/v/pyope/badge.png
.. _order-preserving encryption: https://crypto.stackexchange.com/questions/3813/how-does-order-preserving-encryption-work
.. _Boldyreva's paper: http://www.cc.gatech.edu/~aboldyre/papers/bclo.pdf
