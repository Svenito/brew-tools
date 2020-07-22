==========
brew-tools
==========

This is the documentation for

::

    ╔╗ ╦═╗╔═╗╦ ╦  ╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╩╗╠╦╝║╣ ║║║───║ ║ ║║ ║║  ╚═╗
    ╚═╝╩╚═╚═╝╚╩╝   ╩ ╚═╝╚═╝╩═╝╚═╝


Welcome to the documentation for Brew-Tools, the CLI toolset for
homebrewers

Brew-Tools is a small commandline utility that offers quick access to a
set of calculators and tools to help homebrewers create their brews.

Granted, the CLI is not everyone's favourite interface, and this is by no means
intended to replace other GUI based tools.

Its aim is to provide simple and quick access to tools that are usually
available in a larger piece of software with all the bells and whistles.
Instead of having to click around a desktop app, or wait for web pages to load,
you can complete these tasks very quickly with Brew-tools.

For example to calculate the amount of priming sugar needed

.. code:: bash

    $> brew-tools prime
    Volume of beer to prime (liter): 19
    Desired volumes of CO2: 2.3
    Temperature of beer (C): 15

    Use only one of the following:
    Table sugar: 98.50g
    Corn Sugar: 108.29g
    DME: 144.84g

All values can also be passed in as arguments directly

.. code:: bash

    $> brew-tools prime -beer 19 -vol 2.3 -temp 15

    Use only one of the following:
    Table sugar: 98.50g
    Corn Sugar: 108.29g
    DME: 144.84g


It is written in Python 3 and has minimal dependencies on external packages.

Brew-tools is opensource and contributions and suggestions are welcomed.

.. note::

    All values and calculations are provided as guidelines only.
    Brew-tools should not be used for professional brewing. No warranty
    or guarantee of accuracy is provided on the information provided by
    this calculator.

Contents
========

.. toctree::
   :maxdepth: 2

   Features <features>
   Install <install>
   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

