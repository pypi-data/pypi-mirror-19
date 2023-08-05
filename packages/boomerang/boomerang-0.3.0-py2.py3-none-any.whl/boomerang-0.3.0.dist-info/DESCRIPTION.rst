===============================
Boomerang
===============================


.. image:: https://img.shields.io/pypi/v/boomerang.svg
        :target: https://pypi.python.org/pypi/boomerang

.. image:: https://img.shields.io/travis/kdelwat/boomerang.svg
        :target: https://travis-ci.org/kdelwat/boomerang

.. image:: https://readthedocs.org/projects/boomerang/badge/?version=latest
        :target: https://boomerang.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/kdelwat/boomerang/shield.svg
     :target: https://pyup.io/repos/github/kdelwat/boomerang/
     :alt: Updates


An asynchronous Python library for building services on the Facebook Messenger Platform


* Free software: MIT license
* Documentation: https://boomerang.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.3.0 (4-2-2017)
----------------

- Add automatic attachment hosting using the internal server
- Add proper handling of Messenger API errors

0.2.1 (1-2-2017)
----------------

- Update dependency versions to fix VersionConflict in Travis CI.

0.2.0 (1-2-2017)
----------------

- Implement the Send API. All non-beta templates and messages are supported
  (except for the airline templates).

0.1.0 (25-12-2016)
------------------

- Implement the Webhook API, with handling of all non-beta event types
  excepting the 'message echo' event, which will be added upon completion of
  the Send API implementation.

0.0.0 (22-12-2016)
------------------

- Initial development version.


