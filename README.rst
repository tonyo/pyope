pyope
=====

|PyPi version| |Travis build|

This is an implementation of Boldyreva symmetric `order-preserving encryption`_ scheme (`Boldyreva's paper`_). 

**Disclaimer 1** This is a work in progress, which should be reviewed and evaluated before using in production and/or
sensitive applications. If you have any concerns about used cryptographic primitives or specific implementation
details, feel free to open a Github issue and we'll discuss everything there.

**Disclaimer 2** The Boldyreva scheme is not a standardized algorithm, so there are no test vectors and fixed plaintext-ciphertext
mapping for a given key. It means that, generally speaking, a plaintext encrypted by two different versions of the package
with the same key might not be equal to each other.

Quick examples
--------------

Quick start
::

  from pyope.ope import OPE
  cipher = OPE(b'key goes here')
  assert cipher.encrypt(1000) < cipher.encrypt(2000) < cipher.encrypt(3000)
  assert cipher.decrypt(cipher.encrypt(1337)) == 1337


You can specify input and output ranges. Otherwise, default input (0..2^15-1) and output (0..2^31-1) ranges are used.
::

  from pyope.ope import OPE, ValueRange
  cipher = OPE(b'long key' * 2, in_range=ValueRange(-100, 100),
                                out_range=ValueRange(0, 9999))
  assert 0 < cipher.encrypt(10) < cipher.encrypt(42) < 9999



About order-preserving encryption
---------------------------------

Order-preserving encryption (OPE) allows to compare ciphertext values in order to learn the corresponding relation
between the underlying plaintexts. The algorithm implemented in this package (Boldyreva's method) is **less secure**
than any deterministic encryption schemes or modes (such as ECB), because this scheme is deterministic by design (i.e.,
for a certain key equal plaintext are always mapped to a single ciphertext value).

How can OPE be useful? For example, some systems may need OPE to perform a certain set of queries (such as range SQL
queries) over encrypted data. These systems include `CryptDB`_ and `Monomi`_ to name a few.

Security
--------

As mentioned above, security guarantees for Boldyreva's schema are weaker than those of deterministic encryption schemes,
but security can still be improved if the encryption keys are long enough. It is advised to use randomly generated keys at
least 128 bits long, with the optimal size being equal to 256 bits. Keys can be longer, but it won't improve the overall
security.


Running tests
-------------

PyTest is used as a test framework. Run all tests:

::

$ py.test tests/

TODO
----

- More tests
- Optimize speed
- Security guarantees
- Test on x86

.. |PyPi version| image:: https://img.shields.io/pypi/v/pyope.svg
   :target: https://pypi.python.org/pypi/pyope/
.. |Travis build| image:: https://travis-ci.org/rev112/pyope.svg?branch=master
   :target: https://travis-ci.org/rev112/pyope/
.. _order-preserving encryption: https://crypto.stackexchange.com/questions/3813/how-does-order-preserving-encryption-work
.. _Boldyreva's paper: http://www.cc.gatech.edu/~aboldyre/papers/bclo.pdf
.. _CryptDB: http://css.csail.mit.edu/cryptdb/
.. _Monomi: http://people.csail.mit.edu/nickolai/papers/tu-monomi.pdf

