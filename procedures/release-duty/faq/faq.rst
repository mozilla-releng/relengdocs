FAQ
===

This piece of docs tracks frequently-asked-questions during our releaseduty cycles.

Adding a new locale into Product-Details
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Product details`_ is a public JSON API which contains release
information for Mozilla products. More information on this can be found
in `here`_.

Each time a new locale is being added so that we’re able to
ship a newly-localized Firefox in a different language, RelEng gets involved.
In order for that to happen, the l10n team adds the corresponding builds as a
pre-requisite. Then, they likely ping releaseduty: PR like `this`_ or
`this <https://github.com/mozilla-releng/product-details/pull/9>`__ are
opened against Product-details.

TODO for releaseduty:
- double-check that the PR is listing another
locale in the ``public/1.0/languages.json`` file. See samples PRs like `this`_ or
`this <https://github.com/mozilla-releng/product-details/pull/9>`__ from the past
- review and merge the PR, either directly into ``production``
or via ``main`` and then follow-up with a push to ``production``
- wait for the Taskcluster CI to run successfully. Behind the scenes, the CI is
cloning the repo resources and pushes them to a S3 bucket
- once the CI is green, trigger the Product-Details rebuild via Ship-it: |product-details-rebuild|

.. _Product details: https://product-details.mozilla.org/1.0/
.. _here: https://wiki.mozilla.org/Release_Management/Product_details
.. _this: https://github.com/mozilla-releng/product-details/pull/10
.. |product-details-rebuild| image:: /procedures/release-duty/faq/media/product-details-rebuild.png
