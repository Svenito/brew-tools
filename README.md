brew-tools
==========

```
╔╗ ╦═╗╔═╗╦ ╦  ╔╦╗╔═╗╔═╗╦  ╔═╗
╠╩╗╠╦╝║╣ ║║║───║ ║ ║║ ║║  ╚═╗
╚═╝╩╚═╚═╝╚╩╝   ╩ ╚═╝╚═╝╩═╝╚═╝
```
[![Build Status](https://travis-ci.com/Svenito/brew-tools.svg?branch=main)](https://app.travis-ci.com/github/Svenito/brew-tools)
[![Documentation Status](https://readthedocs.org/projects/brew-tools/badge/?version=latest)](https://brew-tools.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/brew-tools.svg)](https://badge.fury.io/py/brew-tools)

A command line utility that offers a set of calculators for home brewers.

> NOTE: All values and calculations are provided as guidelines only.
> Brew-tools should not be used for professional brewing. No warranty or guarantee of
> accuracy is provided on the information provided by this calculator.

Description
===========

Need to do a quick calculation during your brew day?
Don't fancy digging through a GUI application, or a web based tool?
Prefer to do simple things in a terminal?

Then **brew-tools** is for you.

Currently brew-tools includes:

* ABV calculator
* Keg priming calculator
* Priming sugar calculator
* Quick infusion calculator
* Adjust gravity with dme calculator
* Apparent and Real attenuation calculator
* Final gravity from a given attenuation percentage
* Gravity adjustment by boil off/dilution calculator
* New gravity after volume adjustment
* Strike water temp calculator
* Strike water temperature
* Simple unit converter

More to come

See the [changelog](CHANGELOG.rst) for updates in each version

Installation
============

Brew-tools is available from PyPI

    pip install brew-tools

You can also clone/download this repository and install it using pip

    cd <brew-tools-dir>
    pip install .

Usage
=====

When first starting Brew tools you will be asked for your preferred unit type, metric or imperial.
This is then stored in a config file and used as the default unit. This can be temporarily
changed with the `--unit` option.

Brew tools has built in help

```
Usage: brew_tools [OPTIONS] COMMAND [ARGS]...

  Brew-Tools is a small commandline utility that offers quick access to a
  set of calculators and tools to help homebrewers create their brews.

  All values and calculations are provided as guidelines only. Brew-tools
  should not be used for professional brewing. No warranty or guarantee of
  accuracy is provided on the information provided by this calculator.

Options:
  --version  Show the version and exit.
  --unit [metric|imperial]  Ignore config and use a different unit.
  --help     Show this message and exit.

Commands:
  abv             Calculates the ABV from the original and final gravity...
  adjust-gravity  Calculate the amount of liquid to boil off/dilute with to...
  adjust-volume   Calculate the new gravity after a change in wort volume...
  attenuation     Calculates the apparent and real attenuation from the...
  convert         Convert a value between given measurements.
  dme             Given the current volume of the mash, work out how much...
  fg-from-att     Given a starting gravity and a desired attenuation level,...
  infuse          Given the current mash temperature, work out how much...
  kegpsi          Calculates the regulator pressure required to achieve...
  prime 
```

and also for its commands

```
brew-tools infuse --help
Usage: brew-tools infuse [OPTIONS]

Options:
  -temp FLOAT    Current temperature of mash
  -target FLOAT  Target temperature of mash
  -ratio FLOAT   Grist/water ratio
  -grain FLOAT   Weight of grain in mash
  -water FLOAT   Temp of infusion water
  --help         Show this message and exit.
```

If the inputs are not passed via the command line arguments, brew tools will
prompt the user for input.

For more information see the [documentation](https://brew-tools.readthedocs.io/en/latest/)

Development
===========

If you want to help develop brew tools you should install it into a
virtual environment. The current version of brew-tools uses [Rye](https://rye.astral.sh/) 
to manage virtual environments and such.

In order to start, [install Rye](https://rye.astral.sh/guide/installation/)
and change into the brew-tools directory. From there you can run

    rye sync

which will create a virtual environment and install the dependencies as well as install
`brew_tools` to the environment.
To run `brew_tools` in the development environment run

    rye run brew_tools

Which will launch  `brew_tools`. Simply add arguments to the end of the line.

To run the tests you use

    rye test

In addition to the tests it's advisable to run a linter of the source as Travis
will also check for linting errors.

    rye lint

Thanks
======

Thanks to

* /u/DAMNIT_REZNO - for inspiring me to start this project
* SlayterDev - DME addition calculator
* Szczyp - Add input for grain temp and fix missing input function

License
=======

Brew Tools is released under the MIT license.

See `LICENSE.txt` for more details
