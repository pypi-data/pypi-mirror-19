fastecdsa
=========
.. image:: https://travis-ci.org/AntonKueltz/fastecdsa.svg?branch=master
    :target: https://travis-ci.org/AntonKueltz/fastecdsa
.. image:: https://badge.fury.io/py/fastecdsa.svg
    :target: https://badge.fury.io/py/fastecdsa
.. image:: https://readthedocs.org/projects/fastecdsa/badge/?version=latest
    :target: https://fastecdsa.readthedocs.io/en/latest/

About
-----
This is a python package for doing fast elliptic curve cryptography, specifically
digital signatures.

Security
--------
I am not aware of any current issues. There is no nonce reuse, no branching on secret material,
and all points are validated before any operations are performed on them. Timing side challenges
are mitigated via Montgomery point multiplication. Nonces are generated per RFC6979. That being
said crypto is tricky and I'm not beyond making mistakes. Please use a more established and
reviewed library for security critical applications. Open an issue or email me if you see any
seurity issue or risk with this library.

Python Versions Supported
-------------------------
The initial release of this package was targeted at python2.7. Earlier versions may work but have
no guarantee of correctness or stability. As of release 1.2.1+ python3 is now supported as well.

Supported Primitives
--------------------
Curves over Prime Fields
~~~~~~~~~~~~~~~~~~~~~~~~
* P192 (:code:`fastecdsa.curve.P192`)
* P224 (:code:`fastecdsa.curve.P224`)
* P256 (:code:`fastecdsa.curve.P256`)
* P384 (:code:`fastecdsa.curve.P384`)
* P521 (:code:`fastecdsa.curve.P521`)
* secp256k1 (bitcoin curve) (:code:`fastecdsa.curve.secp256k1`)

Curves over Binary Fields
~~~~~~~~~~~~~~~~~~~~~~~~~
* K163 (:code:`fastecdsa.curve.K163`)
* K233 (:code:`fastecdsa.curve.K233`)
* K283 (:code:`fastecdsa.curve.K283`)
* K409 (:code:`fastecdsa.curve.K409`)
* K571 (:code:`fastecdsa.curve.K571`)

Hash Functions
~~~~~~~~~~~~~~
Any hash function in the :code:`hashlib` module (:code:`md5, sha1, sha224, sha256, sha384, sha512`)
will work, as will any hash function that implements the same interface / core functionality as the
those in :code:`hashlib`. For instance, if you wish to use SHA3 as the hash function the
:code:`pysha3` package will work with this library as long as it is at version >=1.0b1 (as previous
versions didn't work with the :code:`hmac` module which is used in nonce generation).

Performance
-----------

Curves over Prime Fields
~~~~~~~~~~~~~~~~~~~~~~~~
Currently it does basic point multiplication significantly faster than the :code:`ecdsa`
package. You can see the times for 1,000 signature and verification operations below,
:code:`fast.py` corresponding to this package and :code:`regular.py` corresponding
to :code:`ecdsa` package.

.. image:: http://i.imgur.com/oNOfnG6.png?1

As you can see, this package in this case is ~25x faster.

Curves over Binary Fields
~~~~~~~~~~~~~~~~~~~~~~~~~
Curves over binary fields are slower. This is mainly because there are no good C libraries that I
could find optimized for binary fields (e.g. FLINT_ only supports polynomials in a field of
arbitrary characteristic, which means no optimizations and more cases than we need for binary
fields). So the binary field C code is written by me. Finding the inverse of a polynomial is the
main bottleneck currently taking about 50ms (for comparison, signature generation and verification
in prime fields are both <5ms). This will be improved when I have time to optimize (or feel free to
fork and optimize the code).

Installing
----------
You can use pip: :code:`$ pip install fastecdsa` or clone the repo and use
:code:`$ python setup.py install`. Note that you need to have a C compiler.
You  also need to have GMP_ on your system as the underlying
C code in this package includes the :code:`gmp.h` header (and links against gmp
via the :code:`-lgmp` flag). On debian you can install all dependencies as follows:

.. code:: bash

    $ sudo apt-get install python-dev libgmp3-dev

Usage
-----
Generating Keys
~~~~~~~~~~~~~~~
You can use this package to generate keys if you like. Recall that private keys on elliptic curves
are integers, and public keys are points i.e. integer pairs.

.. code:: python

    from fastecdsa import keys, curve

    # generate a private key for curve P256
    priv_key = keys.gen_private_key(curve.P256)

    # get the public key corresponding to the private key we just generated
    pub_key = keys.get_public_key(priv_key, curve.P256)
    (Qx, Qy) = pub_key  # recall that pub_key is simply an integer pair


Signing and Verifying
~~~~~~~~~~~~~~~~~~~~~
Some basic usage is shown below:

.. code:: python

    from fastecdsa import curve, ecdsa, keys
    from hashlib import sha384

    m = "a message to sign via ECDSA"  # some message

    ''' use default curve and hash function (P256 and SHA2) '''
    private_key = keys.gen_private_key(curve.P256)
    public_key = keys.get_public_key(private_key, curve.P256)
    # standard signature, returns two integers
    r, s = ecdsa.sign(m, private_key)
    # should return True as the signature we just generated is valid.
    valid = ecdsa.verify((r, s), m, public_key)

    ''' specify a different hash function to use with ECDSA '''
    r, s = ecdsa.sign(m, private_key, hashfunc=sha384)
    valid = ecdsa.verify((r, s), m, public_key, hashfunc=sha384)

    ''' specify a different curve to use with ECDSA '''
    private_key = keys.gen_private_key(curve.P224)
    public_key = keys.get_public_key(private_key, curve.P224)
    r, s = ecdsa.sign(m, private_key, curve=curve.P224)
    valid = ecdsa.verify((r, s), m, public_key, curve=curve.P224)

    ''' using SHA3 via pysha3>=1.0b1 package '''
    import sha3  # pip install [--user] pysha3==1.0b1
    from hashlib import sha3_256
    private_key, public_key = keys.gen_keypair(curve.P256)
    r, s = ecdsa.sign(m, private_key, hashfunc=sha3_256)
    valid = ecdsa.verify((r, s), m, public_key, hashfunc=sha3_256)

.. _FLINT: http://flintlib.org/
.. _GMP: https://gmplib.org/
