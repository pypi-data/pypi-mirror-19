=====================================
tox-travis: Integrate Tox into Travis
=====================================

.. image:: https://img.shields.io/pypi/v/tox-travis.svg
    :target: https://pypi.python.org/pypi/tox-travis
    :alt: Latest Version

.. image:: https://travis-ci.org/ryanhiebert/tox-travis.svg?branch=master
    :target: https://travis-ci.org/ryanhiebert/tox-travis

.. image:: https://badges.gitter.im/ryanhiebert/tox-travis.svg
   :alt: Join the chat at https://gitter.im/ryanhiebert/tox-travis
   :target: https://gitter.im/ryanhiebert/tox-travis?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

tox-travis is a simple plugin for tox that allows you to use
Travis CI's multiple python version feature as well as tox's
full configurability in a straightforward way.


Usage
=====

Configure the Python versions to test with in ``travis.yml``:

.. code-block:: yaml

    sudo: false
    language: python
    python:
      - "2.7"
      - "3.4"
    install: pip install tox-travis
    script: tox

And it will run the appropriate testenvs,
which by default are any declared env with
``py27`` or ``py34`` as factors of the name.
If no environments match a given factor,
the ``py27`` or ``py34`` envs are used as a fallback.


Advanced Configuration
======================

To customize what environments tox will run on Travis,
add a section to ``tox.ini`` telling it what environments
to run under which versions of Python:

.. code-block:: ini

    [tox]
    envlist = py{27,34}-django{17,18}, docs

    [travis]
    python =
      2.7: py27
      3.4: py34, docs

This would run the Python 2.7 variants under 2.7,
and the Python 3.4 variants and the ``docs`` env under 3.4.

Note that Travis won't run all the envs simultaneously,
because it's build matrix is only aware of the Python versions.
Only one Travis build will be run per Python version,
unless other settings are specified in the Travis build matrix.

If you are using multiple Travis factors,
then you can use those factors to decide what will run.
For example, see the following ``.travis.yml`` and ``tox.ini``:

.. code-block:: yaml

    sudo: false
    language: python
    python:
      - "2.7"
      - "3.4"
    env:
      - DJANGO="1.7"
      - DJANGO="1.8"
    include:
      - os: osx
        language: generic
    install: pip install tox-travis
    script: tox


.. code-block:: ini

    [tox]
    envlist = py{27,34}-django{17,18}, docs

    [travis]
    os =
      linux: py{27,34}-django{17,18}, docs
      osx: py{27,34}-django{17,18}
    python =
      3.4: py34, docs

    [travis:env]
    DJANGO =
      1.7: django17
      1.8: django18, docs

Travis will run 5 different jobs,
which will each run jobs as specified by the factors given.

* os: linux (default), language: python, python: 2.7, env: DJANGO=1.7

  This will run the env ``py27-django17``,
  because ``py27`` is the default,
  and ``django17`` is specified.

* os: linux (default), language: python, python: 3.4, env: DJANGO=1.7

  This will run the env ``py34-django17``,
  but not ``docs``,
  because ``docs`` is not included in the DJANGO 1.7 configuration.

* os: linux (default), language: python, python: 2.7, env: DJANGO=1.8

  This will run the env ``py27-django18``,
  because ``py27`` is the default.
  ``docs`` is not run,
  because Python 2.7 doesn't include ``docs``
  in the defaults that are not overridden.

* os: linux (default), language: python, python: 3.4, env: DJANGO=1.8

  This will run the envs ``py34-django18`` and ``docs``,
  because all specified factors match,
  and ``docs`` is present in all related factors.

* os: osx, language: generic

  This will run envs ``py27-django17``, ``py34-django17``,
  ``py27-django18``, and ``py34-django18``,
  because the ``os`` factor is present,
  and limits it to just those envs.


After All
=========

Inspired by `travis-after-all`_ and `travis_after_all`_,
this feature allows a job to wait for other jobs to finish
before it calls itself complete.

.. _`travis-after-all`: https://github.com/alrra/travis-after-all
.. _`travis_after_all`: https://github.com/dmakhno/travis_after_all

There are three environment variables
that can be used to configure this feature.

* ``GITHUB_TOKEN``. This is *required*,
  and should be encrypted in the ``.travis.yml``.
  This is used as the authentication method
  for the Travis CI API.
* ``TRAVIS_POLLING_INTERVAL``.
  How often, in seconds, we should check the API
  to see if the rest of the jobs have completed.
  Defaults to 5.
* ``TRAVIS_API_URL``.
  The base URL to the Travis API for this build.
  This defaults to ``https://api.travis-ci.org``.
  A common override will be to the commercial version,
  at ``https://api.travis-ci.com``.

Configure which job to wait on by adding
the ``[travis:after]`` section to the ``tox.ini`` file.
The ``travis`` key looks for values that would be keys
in various items in the ``[travis]`` section,
and the ``env`` key looks for values that would be keys
in items in the ``[travis:env]`` section.

For example:

.. code-block:: ini

    [travis:after]
    travis = python: 3.5
    env = DJANGO: 1.8

Then run ``tox`` in your test command like this::

   tox --travis-after

For example, consider this mocked up ``.travis.yml``,
that corresponds to using the above ``travis:after`` section:

.. code-block:: yaml

    sudo: false
    language: python
    python:
      - "2.6"
      - "3.5"
    env:
      global:
        - GITHUB_TOKEN='spamandeggs'  # Make sure this is encrypted!
      matrix:
        - DJANGO="1.7"
        - DJANGO="1.8"
    install: pip install tox-travis
    script: tox --travis-after
    deploy:
      provider: pypi
      user: spam
      password: eggs  # Make sure to encrypt passwords!
      on:
        tags: true
        python: 3.5
        condition: DJANGO = "1.8"
      distributions: sdist bdist_wheel

This example deploys when the build is from a tag
and the build is on Python 3.5
and the build is using DJANGO="1.8".
Together ``tox --travis-after`` and Tox's ``on`` conditions
make sure that the deploy only happens after all tests pass.

If any configuration item does not match,
or if no configuration is given,
this will run exactly as it would normally.
However, if the configuration matches the current job,
then it will wait for all the other jobs to complete
before it will be willing to return a success return code.

If the tests fail, then it will not bother waiting,
but will rather return immediately.
If it determines that another required job has failed,
it will return an error indicating that jobs failed.

You can use this together with a deployment configuration
to ensure that this job is the very last one to complete,
and will only be successful if all others are successful,
so that you can be more confident
that you are shipping a working release.

The accepted configuration keys
in the ``[travis:after]`` section are:

* ``toxenv``. Match with the running toxenvs,
  based on the ``TOXENV`` environment variable,
  which is set automatically by Tox-Travis.
  Expansion is allowed, and if set *all* environments listed
  must be present in the ``TOXENV`` environment variable.
* ``travis``. Match with known Travis factors,
  as is done in the ``[travis]`` section.
  For instance, specifying that we should wait
  when python is version 2.7 would look like
  ``travis = python: 2.7``.
* ``env``. Match with environment variable factors,
  as might be specified in the ``[travis:env]`` section.
  For instance, if we want to match that ``DJANGO`` is ``1.9``,
  then it would look like ``env = DJANGO: 1.9``.
  The value must match exactly to succeed.


0.7 (2016-12-20)
+++++++++

* Deprecate the ``[tox:travis]`` section in favor of
  the ``python`` key to the new ``[travis]`` section.
* Allow specifying envs by other Travis factors.
  Includes ``os``, ``language``, and ``python``.
* Allow specifying envs for environment variables,
  in a new ``[travis:env]`` section.
* Special thanks to @rpkibly for driving this work (#34)
* Backward incompatible changes:

  * If *any* declared tox envs match the envs matched from factors,
    no additional envs will be included automatically.
    For example, if ``envlist`` is ``docs``,
    and the configuration for python 3.4 is ``py34, docs``,
    it previously would have run both the declared ``docs`` env,
    as well as the undeclared ``py34`` env,
    while now it will only run the declared ``docs`` env.
    This may result in *fewer* envs running than expected,
    but in edge cases that were believed to be unlikely.
  * Previously, if no Python version was given in the environment,
    it would automatically choose an appropriate env
    based on the Python version running.
    Now if no Python version is given in the environment
    no env is determined by default,
    which may result in *more* envs running in a job than expected.

* Add the ``--travis-after`` command to enable
  a job to wait until all others have completed. (#13)
  - thanks to @ssbarnea for the feature suggestion.

0.6 (2016-10-13)
++++++++++++++++

* Require pytest<3 for Python 3.2 (#33)

0.5 (2016-07-28)
++++++++++++++++

* Prefer ``TRAVIS_PYTHON_VERSION`` to sys.version_info (#14)
  - thanks to @jayvdb for the code review
* Add Python 3.2 support (#17)
  - thanks to @jayvdb for the bug report, discussion, and code review
* Support PyPy3 v5.2 with setuptools hackery (#24)
  - thanks to @jayvdb for the pull request

0.4 (2016-02-10)
++++++++++++++++

* Generate default env from sys.version_info (#9)
  - thanks to @jayvdb for the bug report


0.3 (2016-01-26)
++++++++++++++++

* Match against testenvs that are only declared as sections (#7)
  - thanks to @epsy
* Include unmatched envs verbatim to run (also #7)
  - thanks to @epsy again


0.2 (2015-12-10)
++++++++++++++++

* Choose testenvs from ``tox.ini`` by matching factors.

  * This is a slightly *backward incompatible* change
  * If a Python version isn't declared in the ``tox.ini``,
    it may not be run.
  * Additional envs may be run if they also match the factors,
    for example, ``py34-django17`` and ``py34-django18`` will
    both match the default for Python 3.4 (``py34``).
  * Factor matching extends to overrides set in ``tox.ini``.


0.1 (2015-05-21)
++++++++++++++++

* Initial Release


