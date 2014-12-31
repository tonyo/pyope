pyope
=====

This is an implementation of Boldyreva symmetric order-preserving encryption scheme (http://www.cc.gatech.edu/~aboldyre/papers/bclo.pdf).

Quick example
-------------

::

  from pyope.ope import OPE
  cipher = OPE('key goes here')
  assert cipher.encrypt(1000) < cipher.encrypt(2000) < cipher.encrypt(3000)
  assert cipher.decrypt(cipher.encrypt(1337)) == 1337


Running tests
-------------

`$ py.test tests/`

TODO
----

- More tests
- Nice README
- Get rid of numpy dependency (rewrite hypergeometric sampling code?)
- Optimize speed
- PyPi package




