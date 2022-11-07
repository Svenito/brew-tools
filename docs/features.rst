========
Features
========

Brew Tools comes with the following tools (from the help)

.. code:: bash

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
    adjust-sg       Calculate the adjusted single gravity according to the...
    adjust-volume   Calculate the new gravity after a change in wort volume...
    attenuation     Calculates the apparent and real attenuation from the...
    convert         Convert a value between given measurements.
    dme             Given the current volume of the mash, work out how much...
    fg-from-att     Given a starting gravity and a desired attenuation level,...
    infuse          Given the current mash temperature, work out how much...
    kegpsi          Calculates the regulator pressure required to achieve...
    prime           Calculates the amount of table sugar, corn sugar, or DME...
    strike          Calculate the required strike water temperature given...

The full command descriptions are below

abv
###

Calculates the ABV from the original and final gravity readings. By default the wort and alcohol correction factor is not applied.
If you are using a hydrometer add the ``adjust`` flag to automatically correct the final gravity.

adjust-gravity
##############

Calculate the amount of liquid to boil off/dilute with to achieve a desired gravity.

adjust-sg
#########

Temperature correction of single gravity reading

adjust-volume
#############
Calculate the new gravity after a change in wort volume either through dilution or boil off

attenuation
###########

Calculates the apparent and real attenuation from the provided original and final/current gravity.
Real attenuation is the adjusted value taking into account the alcohol in the beer

convert
#######
Convert a value between given measurements. Supported types are:

    mass, volume, gravity, colour

dme
###

Given the current volume of the mash, work out how much Dry Malt Extract(DME) to add to reach your target gravity

fg-from-att
###########

Given a starting gravity and a desired attenuation level, will return the specific gravity for that percentage of attenuation.
Useful if you have to action something at a given attenuation point and need to know what the gravity is when that point is reached

infuse
######

Given the current mash temperature, work out how much water of a given temp needs to be added to adjust the temperature

kegpsi
######

Calculates the regulator pressure required to achieve desired CO2 volumes.

prime
#####

Calculates the amount of table sugar, corn sugar, or DME needed to achieve the requested CO2 volumes for bottle priming

strike
######

Calculate the strike water temperature given the mass of grain, volume    of water, and desired mash temperature

Using brew-tools in your own project
====================================

All these tools are available to use in your own Python application by
importing the ``brew_maths`` module into your code

.. code:: Python

  import brew_maths from brew_tools

  new_gravity = brew_maths.adjust_gravity(1.050, 1.020)

Not that the ``brew_maths`` module does not do any bounds checking on the values
passed. It is up to the calling code to ensure that the values are within valid bounds if needed
