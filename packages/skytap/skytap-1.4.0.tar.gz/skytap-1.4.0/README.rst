=======================
Skytap REST API wrapper
=======================

.. image:: https://img.shields.io/pypi/v/skytap.svg
   :target: https://pypi.python.org/pypi/skytap


.. image:: https://readthedocs.org/projects/skytap/badge/?version=latest
   :target: http://skytap.readthedocs.org/en/latest/
   :alt: Documentation

.. image:: https://travis-ci.org/mapledyne/skytap.svg?branch=master
    :target: https://travis-ci.org/mapledyne/skytap
    :alt: Travis build status

.. image:: https://landscape.io/github/mapledyne/skytap/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mapledyne/skytap/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/github/mapledyne/skytap/badge.svg?branch=master
   :target: https://coveralls.io/github/mapledyne/skytap?branch=master
   :alt: Code coverage


Skytap is a set of modules that we use to manage aspects of our Skytap
infrastructure.

Usage
---------------

To use the module, you'll need to create at least two environment variables::

    SKYTAP_USER=kermit.frog@sesamestreet.net
    SKYTAP_TOKEN=79824879aeb2b34534e112d23a3c

Optionally, you can also add::

    SKYTAP_LOG_LEVEL=20

This can be a number between 0-50 and corresponds to the logging module from Python:

* DEBUG: 0
* INFO: 10
* WARNING: 20
* ERROR: 30
* CRITICAL: 50

An easy way to set these variables is to create a .skytap file in your home directory (~/.skytap) with the variables in there::

    export SKYTAP_USER=kermit.frog@sesamestreet.net
    export SKYTAP_TOKEN=79824879aeb2b34534e112d23a3c

Then you can source the file::

    source ~/.skytap

to load the variables, or add that same source command to your ~/.bash_profile or equivalent file to have it done automatically.

Via the command line
~~~~~~~~~~~~~~~~~~~~

Most modules can be accessed directly from the command line to get simple information. This functionally returns the JSON from the Skytap API::

    python -m skytap.Environments
    python -m skytap.Users

You'll get back a JSON for the request, something like::

    [
      {
        "id": "12345",
        "url": "https://cloud.skytap.com/users/12345",
        "login_name": "kermit.frog@sesamestreet.net",
        "first_name": "Kermit",
        "last_name": "The Frog",
        "title": "Master of Ceremonies",
        "email": "kermit.frog@sesamestreet.net",
        "created_at": "2012-01-02T12:43:05-08:00",
        "deleted": false
      }
    ]

If you only want a one item returned instead of the full list, you can get that from the command line as well::

    python -m skytap.Environments 12345
    python -m skytap.Quotas svm_hours

Via Python script
~~~~~~~~~~~~~~~~~

To use this, simply import it::

    import skytap

Then you can access the resource groups of interest.

A simple example::

    import skytap
    users = skytap.Users()
    for u in users:
        print(u.name + ' : ' + u.email)

This can also help automate running and suspending VMs::

    import skytap
    envs = skytap.Environments()

    envs[123456].suspend()  # or .suspend(True) if you want the script to wait.

Doing this will, by default, add a note to the environment of it's action, so someone checking the environment can see why it's not running.

Installation
------------

Install this through pip::

    pip install skytap

Contributor list
----------------

* Bill Wellington `github <https://github.com/thewellington/>`__ `twitter <https://twitter.com/CollectiveWe>`__ `blog <http://www.wellingtonnet.net>`__
* Michael Knowles `github <https://github.com/mapledyne>`__ `twitter <https://twitter.com/Mapledyne>`__ `blog <http://mapledyne.com>`__
* Caleb Hawkins `github <https://github.com/calebh93>`__ `twitter <https://twitter.com/MuddyTM>`__ `blog <http://calebh93.github.io>`__

Contact us directly for questions.
