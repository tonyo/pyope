pyope
=====

|PyPi version| |Travis build|

This is an implementation of Boldyreva symmetric `order-preserving encryption`_ scheme (`Boldyreva's paper`_).

Supported Python versions: 2.7 and 3.5+

**Disclaimer 1** This is an experimental implementation, which should be thoroughly reviewed and evaluated before using in production and/or sensitive applications.

**Disclaimer 2** The Boldyreva scheme is not a standardized algorithm, so there are no test vectors and fixed plaintext-ciphertext
mapping for a given key. It means that, generally speaking, a plaintext encrypted with the same key by two different versions of the package might not be equal to each other.

Installation
------------

.. code:: shell

  pip install pyope

Examples
--------------

Quick start

.. code:: python

  from pyope.ope import OPE
  random_key = OPE.generate_key()
  cipher = OPE(random_key)
  assert cipher.encrypt(1000) < cipher.encrypt(2000) < cipher.encrypt(3000)
  assert cipher.decrypt(cipher.encrypt(1337)) == 1337


You can specify input and output ranges. Otherwise, default input (0..2^15-1) and output (0..2^31-1) ranges are used.

.. code:: python

  from pyope.ope import OPE, ValueRange
  cipher = OPE(b'long key' * 2, in_range=ValueRange(-100, 100),
                                out_range=ValueRange(0, 9999))
  assert 0 < cipher.encrypt(10) < cipher.encrypt(42) < 9999


About order-preserving encryption
---------------------------------

Order-preserving encryption (OPE) allows to compare ciphertext values in order to learn the corresponding relation
between the underlying plaintexts. By definition, order-preserving encryption methods are **less secure** than
conventional encryption algorithms for the same data sizes, because the former leak ordering information of the plaintext 
values.

How can OPE be useful? For example, some systems may need OPE to perform a certain set of queries (such as range SQL
queries) over encrypted data. These systems include `CryptDB`_ and `Monomi`_ to name a few.

Security
--------

As mentioned above, security guarantees for Boldyreva's schema are weaker than those of deterministic encryption schemes,
but security can still be improved if the encryption keys are long enough. It is advised to use randomly generated keys at
least 256 bits long.


Running tests
-------------

PyTest is used as a test framework. Run all tests:

::

$ py.test tests/

TODO
----

- More tests
- Optimize performance
- Security guarantees?

.. |PyPi version| image:: https://img.shields.io/pypi/v/pyope.svg
   :target: https://pypi.python.org/pypi/pyope/
.. |Travis build| image:: https://travis-ci.org/tonyo/pyope.svg?branch=master
   :target: https://travis-ci.org/tonyo/pyope/
.. _order-preserving encryption: https://crypto.stackexchange.com/questions/3813/how-does-order-preserving-encryption-work
.. _Boldyreva's paper: http://www.cc.gatech.edu/~aboldyre/papers/bclo.pdf
.. _CryptDB: http://css.csail.mit.edu/cryptdb/
.. _Monomi: http://people.csail.mit.edu/nickolai/papers/tu-monomi.pdf

