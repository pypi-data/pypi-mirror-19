README
======

.. image:: https://travis-ci.org/david415/pylioness.png?branch=master
    :target: https://www.travis-ci.org/david415/pylioness
    :alt: travis

.. image:: https://coveralls.io/repos/github/david415/pylioness/badge.svg?branch=master
    :target: https://coveralls.io/github/david415/pylioness
    :alt: coveralls



Warning
=======
This code has not been formally audited by a cryptographer. It therefore should not
be considered safe or correct. Use it at your own risk!


overview
--------

pylioness is a parameterized implementation of the LIONESS wide block cipher.
Use it with AES in counter mode + Sha256 or Chacha20 + Blake2b.


details
-------

Lioness is a wide block cipher composed using a stream cipher and a keyed hash function.

read the Lioness paper:
**Two Practical and Provably Secure Block Ciphers: BEAR and LION**
*by Ross Anderson and Eli Biham*

https://www.cl.cam.ac.uk/~rja14/Papers/bear-lion.pdf


pylioness is a parameterized implementation of the LIONESS wide block
cipher which can utilize any stream cipher and keyed digest as long as
the digest output is equal to the stream cipher key size. We've
provided an AES in counter mode + SHA256 and Chacha20 + Blake2b Lioness
implementations with code samples and verified unit test vectors.
