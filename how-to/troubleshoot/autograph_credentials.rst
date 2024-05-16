Autograph Credentials
=====================

Autograph uses `hawk`_ for authentication. Each ``hawk`` user, has access to
one or more autograph *signers*. When making a signing request,
`signingscript`_ can choose which signer to use by specifying a ``keyid``. If
no ``keyid`` is specified, Autograph will use the "default" signer.

.. note::

   It's not entirely clear how Autograph chooses a default signer. Therefore
   it's best practice to always specify a ``keyid`` in signingscript. This also
   makes it more explicit about which signer is being used when reading the
   signingscript configs.


Unfortunately, ``signingscript`` often relies on this default behaviour, which
means it isn't possible to tell what signer is being used under the hood, just
by reading the configs. One possibility for finding this information, is to
trace back to the original request, and hope that it was left in a bug comment
or similar.

Luckily there's a better option. Hal maintains some dumps of the Autograph
database in a `datasette dashboard`_. Specifically `this view`_ maps ``hawk``
user to ``signer``. The default signer is (likely) the record with the lowest
``rowId``.


.. _hawk: https://github.com/mozilla/hawk
.. _signingscript: https://github.com/mozilla-releng/scriptworker-scripts/tree/master/signingscript
.. _datasette dashboard: https://lite.datasette.io/?csv=https://gist.githubusercontent.com/hwine/9949f9e58dd514161cbecf7e6263a01a/raw/prod-signers.csv&csv=https://gist.githubusercontent.com/hwine/9949f9e58dd514161cbecf7e6263a01a/raw/prod-authorizations_edge.csv&csv=https://gist.githubusercontent.com/hwine/9949f9e58dd514161cbecf7e6263a01a/raw/prod-authorizations_app.csv#/data
.. _this view: https://lite.datasette.io/?csv=https://gist.githubusercontent.com/hwine/9949f9e58dd514161cbecf7e6263a01a/raw/prod-signers.csv&csv=https://gist.githubusercontent.com/hwine/9949f9e58dd514161cbecf7e6263a01a/raw/prod-authorizations_edge.csv&csv=https://gist.githubusercontent.com/hwine/9949f9e58dd514161cbecf7e6263a01a/raw/prod-authorizations_app.csv#/data/prod-authorizations_app
