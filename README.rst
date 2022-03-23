brew-tools
==========

::

    ╔╗ ╦═╗╔═╗╦ ╦  ╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╩╗╠╦╝║╣ ║║║───║ ║ ║║ ║║  ╚═╗
    ╚═╝╩╚═╚═╝╚╩╝   ╩ ╚═╝╚═╝╩═╝╚═╝

|Build Status| |Documentation Status| |PyPI version|

A command line utility that offers a set of calculators for home
brewers.

    NOTE: All values and calculations are provided as guidelines only.
    Brew-tools should not be used for professional brewing. No warranty
    or guarantee of accuracy is provided on the information provided by
    this calculator.

Description
===========

Need to do a quick calculation during your brew day? Don't fancy digging
through a GUI application, or a web based tool? Prefer to do simple
things in a terminal?

Then **brew-tools** is for you.

Currently brew-tools includes:

-  ABV calculator
-  Keg priming calculator
-  Priming sugar calculator
-  Quick infusion calculator
-  Adjust gravity with dme calculator
-  Apparent and Real attenuation calculator
-  Final gravity from a given attenuation percentage
-  Gravity adjustment by boil off/dilution calculator
-  New gravity after volume adjustment
-  Strike water temperature
-  Unit conversion

More to come

See the `changelog <CHANGELOG.rst>`__ for updates in each version

Installation
============

Brew-tools is available from PyPI

::

    pip install brew-tools

You can also clone/download this repository and install it using pip

::

    cd <brew-tools-dir>
    pip install .

Usage
=====

When first starting Brew tools you will be asked for your preferred unit type, metric or imperial.
This is then stored in a config file and used as the default unit. This can be temporarily
changed with the `--unit` option.

Brew tools has built in help

::

    Usage: brew-tools [OPTIONS] COMMAND [ARGS]...

    Options:
    --version  Show the version and exit.
    --unit [metric|imperial]  Ignore config and use a different unit.
    --help     Show this message and exit.

    Commands:
    abv
    infuse
    kegpsi
    prime
    dme

and also for its commands

::

    brew-tools infuse --help
    Usage: brew-tools infuse [OPTIONS]

    Options:
      -temp FLOAT    Current temperature of mash
      -target FLOAT  Target temperature of mash
      -ratio FLOAT   Grist/water ratio
      -grain FLOAT   Weight of grain in mash
      -water FLOAT   Temp of infusion water
      --help         Show this message and exit.

If the inputs are not passed via the command line arguments, brew tools
will prompt the user for input.

For more information see the
`documentation <https://brew-tools.readthedocs.io/en/latest/>`__

Development
===========
If you want to help develop brew tools you should install it into a
virtual environment. The current version of brew-tools uses [Poetry](https://poetry.eustace.io/)
to manage virtual environments and such.

In order to start, [install Poetry](https://poetry.eustace.io/docs/#installation)
and change into the brew-tools directory. From there you can run

::

    poetry install

which will create a virtual environment and install the dependencies.
To run `brew_tools` in the developmeent environment it's probably easiest to run

::

    poetry shell

which will spawn a configured shell for the environment.

Tests can be run in this environment, or you can use

::

   poetry run pytest tests

to run the tests without spawning a shell.

In addition to the tests it's advisable to run a linter of the source as Travis
will also check for linting errors. The linter command ignores some errors, so you
can use this command to match the command run by Travis

::

    poetry run flake8 src --ignore=E501,W504,W503

Thanks
======

Thanks to

-  /u/DAMNIT\_REZNO - for inspiring me to start this project
-  SlayterDev - DME addition calculator

License
=======

Brew Tools is released under the MIT license.

See ``LICENSE.txt`` for more details

.. |Build Status| image:: https://travis-ci.com/Svenito/brew-tools.svg?branch=main
   :target: https://travis-ci.com/Svenito/brew-tools
.. |Documentation Status| image:: https://readthedocs.org/projects/brew-tools/badge/?version=latest
   :target: https://brew-tools.readthedocs.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/brew-tools.svg
   :target: https://badge.fury.io/py/brew-tools
