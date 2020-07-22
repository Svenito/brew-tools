========
Features
========

Brew Tools comes with the following tools (from the help)

.. code:: bash

    brew_tools --help                                 [±master ●●]
    Usage: brew_tools [OPTIONS] COMMAND [ARGS]...
    
      Brew-Tools is a small commandline utility that offers quick access to a
      set of calculators and tools to help homebrewers create their brews.
    
      All values and calculations are provided as guidelines only. Brew-tools
      should not be used for professional brewing. No warranty or guarantee of
      accuracy is provided on the information provided by this calculator.
    
    Options:
      --version  Show the version and exit.
      -imperial  Use imperial units. Metric by default.
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
    prime           Calculates the amount of table sugar, corn sugar, or DME...


abv
###

Calculates the ABV from the original and final gravity readings. By default the wort and alcohol correction factor is not applied. 
If you are using a hydrometer add the ``adjust`` flag to automatically correct the final gravity.

adjust-gravity  
##############

Calculate the amount of liquid to boil off/dilute with to achieve a desired gravity.

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
    
