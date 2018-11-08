import math


def oz_to_g(oz):
    """
    Convert ounces to grams
    """
    return oz * 28.34952


def g_to_oz(g):
    """
    Convert grams to ounces
    """
    return g / 28.34952


def lbs_to_oz(lbs):
    """
    Convert lbs to ounces
    """
    return lbs * 16


def c_to_f(c):
    """
    Convert celcius to fahrenheit
    """
    return c * 1.8 + 32.0


def f_to_c(f):
    """
    Convert fahrenheit to celcius
    """
    return 0.55 * (f - 32.0)


def l_to_g(l):
    """
    Convert liters to gallons US
    """
    return l * 0.26417


def g_to_l(g):
    """
    Convert US gallons to liters
    """
    return g / 0.26417


def l_to_q(l):
    """
    Convert liters to quarts US
    """
    return l * 1.056688


def kg_to_lbs(kg):
    """
    Convert kilograms to pounds
    """
    return kg * 2.204623


def to_brix(value):
    """
    Convert gravity value to brix value
    """
    brix = (((182.4601 * value - 775.6821) *
            value + 1262.7794) * value - 669.5622)
    return brix


def to_plato(sg):
    """
    Convert specific gravity to plato (extract)

    (-1 * 616.868) + (1111.14 * sg) – (630.272 * sg^2) + (135.997 * sg^3)
    """
    plato = ((-1 * 616.868) + (1111.14 * sg) -
             (630.272 * sg**2) + (135.997 * sg**3))
    return plato


def to_sg(plato):
    """
    Convert from plato to specific gravity
    """
    return 1 + (plato / (258.6 - ((plato / 258.2) * 227.1)))


def adjust_gravity(og, fg):
    """
    Adjust final gravity for wort correction and alcohol

    :arg og: original gravity as specific gravity
    :arg fg: final gravity as specific gravity
    :returns: adjusted specific gravity value
    """
    adjusted_fg = (1.0000 - 0.00085683 * to_brix(og)) + 0.0034941 * to_brix(fg)
    return adjusted_fg


def abv(og, fg):
    """
    Calculate the ABV from the given ``og`` and ``fg``. Will automatically
    adjust the fg for wort correction and alcohol

    :arg og: The original gravity
    :arg fg: The final gravity
    :returns: The ABV value
    """
    return (og - adjust_gravity(og, fg)) * 131.25


def keg_psi(temp, co2):
    """
    Calculate require keg pressure to carbonate liquid at ``temp`` with
    ``co2`` volumes of CO2

    From http://www.wetnewf.org/pdfs/Brewing_articles/CO2%20Volumes.pdf

    V = (P + 14.695) * ( 0.01821 + 0.09011*EXP(-(T-32)/43.11) ) - 0.003342

    :arg temp: Temperature of liquid in keg in fahrenheit
    :arg co2: Volume of CO2 required
    :returns: The PSI value to set the regulator to
    """
    henry_coeff = 0.01821 + 0.09011 * math.exp(-(temp - 32) / 43.11)
    pressure = ((co2 + 0.003342) / henry_coeff) - 14.695
    return pressure


def priming(temp, beer_vol, co2):
    """
    Calculate the required weight priming (table) sugar for a given
    volume of beer at a specific temperature for desired CO2 volume.
    Beer temperature should be the temperature that the beer has
    been at the longest.

    From: http://www.straighttothepint.com/priming-sugar-calculator/

    PS = 15.195 * Vbeer * (VCO2 - 3.0378 + (0.050062 * Tferm) -
         (0.00026555 * (Tferm ^ 2))

    :arg temp: Temperature of beer in fahrenheit
    :arg beer_vol: Volume of beer to prime in gallons US
    :arg co2: The volume of CO2 required
    :returns: The amount table sugar required
    """
    return (15.195 * beer_vol *
            (co2 - 3.0378 + (0.050062 * temp) -
             (0.00026555 * (temp ** 2))))


def infusion(ratio, curr_temp, new_temp, water_temp, grain):
    """
    Calculate the amount of hot water required to raise the mash
    temperature to a specific temperature.

    From: http://howtobrew.com/book/section-3/the-methods-of-mashing/calculations-for-boiling-water-additions

    Wa = (T2 - T1)(.2G + Wm)/(Tw - T2)

    :arg ratio: Grist ratio in quarts/lbs
    :arg curr_temp: Current mash temperature in fahrenheit
    :arg new_temp: The target temperature of the mash in fahrenheit
    :arg water_temp: The temperature of the water to be added in fahrenheit
    :arg grain: The dry weight of the grain in the mash in pounds
    :returns: The amount of water at given temperature to add to achieve
        requested change in mash temperature
    """
    mash_water = grain * ratio
    return (((new_temp - curr_temp) *
            (0.2 * grain + mash_water)) / (water_temp - new_temp)
            )


def pre_boil_dme(points, cur_vol):
    """
    Calculate the amount of DME needed to raise the gravity of a
    given volume of wort by a given number or gravity points. Assumes
    DME has an extract of 1.044ppg.

    :arg points: Number of gravity points to raise
    :arg cur_vol: The current volume of the wort in gallons.
    :returns: The amount of DME to add to raise the gravity
    """
    return lbs_to_oz(points * (1 / (44 / cur_vol)))


def apparent_attenuation(og, fg):
    """
    Calculate the apparent attenuation from the current and
    original gravity.
    via http://realbeer.com/spencer/attenuation.html

    AA = 1 - AE / OE

    :arg og: The original gravity of the wort (1.0 to 1.2)
    :arg fg: The current gravity of the beer
    :returns: The apparent attenuation as a decimal (multiply
        by 100 to get percentage value)
    """
    return 1.0 - to_plato(fg) / to_plato(og)


def real_attenuation(og, fg):
    """
    Calculate the real attentuation from the original and current
    gravity. Takes into account the alcohol in the beer. Calculates
    the real extract and uses that to calculate the attenuation
    via http://realbeer.com/spencer/attenuation.html

    RE = .1808*OE + .8192*AE
    RA = 1 - RE / OE

    or

    RA = 1 - (.1808*OE + .8192*AE) / OE

    :arg og: The original gravity of the wort (1.0 to 1.2)
    :arg fg: The current gravity of the beer
    :returns: The real attenuation as a decimal (multiply
        by 100 to get percentage value)
    """
    oe = to_plato(og)
    ae = to_plato(fg)

    return 1.0 - (.1808 * oe + .8192 * ae) / oe


def fg_from_attenuation(og, attenuation):
    """
    Calculates the gravity when the beer has reached a given
    attenuation percentage from the original gravity. Simply
    an inverse solve of ``apparent_attenuation``

    :arg og: The original gravity of the wort as specific gravity
    :arg attenuation: The percentage attenuation to achieve
    :returns: The gravity when the requested attenuation has been reached
    """
    fg = (1.0 - (attenuation / 100.0)) * to_plato(og)
    return to_sg(fg)


def adjust_gravity_volume(vol, og, ng):
    """
    Returns the new volume needed to achieve the desired new gravity.
    This is unit independent and the return value can be used for liters
    and or gallons.

    New Volume = (Volume * original Gravity) / new Gravity

    :arg vol: Original volume of wort
    :arg og: The current gravity of the wort
    :arg ng: The desired gravity of the wort
    :returns: The amount to adjust the wort volume by
    """
    og = (og - 1) * 1000
    ng = (ng - 1) * 1000
    return (vol * og) / ng


def adjust_volume_gravity(vol, og, new_vol):
    """
    Calculate the new gravity after boil off or dilution to ``new_vol``
    This is unit independent and the volume can be used for liters
    and or gallons.

    Ending Gravity = (Beginning Volume * Beginning Gravity) / End Volume

    :arg vol: Original volume of wort
    :arg og: The current gravity of the wort
    :arg new_vol: The new volume of the wort
    :returns: The new gravity after boiloff or dilution
    """
    og = (og - 1) * 1000
    return 1 + ((vol * og) / new_vol) / 1000
