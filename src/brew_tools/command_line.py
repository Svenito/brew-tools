
import click

import sys
import logging

from brew_tools import __version__
from brew_tools import inputs
import brew_tools.brew_maths as bm

__author__ = "Sven Steinbauer"
__copyright__ = "Sven Steinbauer"
__license__ = "mit"

_logger = logging.getLogger(__name__)


UNITS = {"metric": {"temp": "C", "weight": "g",
                    "lrg_weight": "kg", "vol": "liter"},
         "imperial": {"temp": "F", "weight": "oz",
                      "lrg_weight": "lbs", "vol": "US Gal"}}


@click.group()
@click.version_option(version=__version__)
@click.option(
    "-imperial",
    help="Use imperial units. Metric by default.",
    is_flag=True,
    default=False
)
@click.pass_context
def main(ctx, imperial):
    """
    Brew-Tools is a small commandline utility that offers quick access to a
    set of calculators and tools to help homebrewers create their brews.

    All values and calculations are provided as guidelines only.
    Brew-tools should not be used for professional brewing. No warranty
    or guarantee of accuracy is provided on the information provided by
    this calculator.
    """
    ctx.ensure_object(dict)
    unit = "metric"
    if imperial:
        unit = "imperial"

    ctx.obj['units'] = UNITS[unit]
    ctx.obj['unit'] = unit


@main.command()
@click.option(
    "-og",
    type=float,
    help="Original Gravity as value between 1.000 and 1.200"
)
@click.option(
    "-fg",
    type=float,
    help="Final Gravity as value between 1.000 and 1.200"
)
@click.pass_context
def abv(ctx, og, fg):
    """
    Calculates the ABV from the original and final gravity readings
    """
    # These prompts are used instead of using the `prompt` attribute in the
    # click options so that it is possible to add units to the end of the
    # prompt based on the requested unit format.
    if not og:
        og = inputs.get_gravity_input(ctx, "Original Gravity: ")
    if not fg:
        fg = inputs.get_gravity_input(ctx, "Final Gravity: ")

    # If passed in via options we need to check valid range
    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og) or not valid_range(fg):
        sys.exit(1)

    if fg > og:
        print("Final gravity cannot be higher than original gravity")
        sys.exit(1)

    print("Estimated ABV: {0:.2f}%".format(bm.abv(og, fg)))


@main.command()
@click.option(
    "-vol",
    type=float,
    help="Desired volumes of CO2"
)
@click.option(
    "-temp",
    type=float,
    help="Temperature of keg"
)
@click.pass_context
def kegpsi(ctx, vol, temp):
    """
    Calculates the regulator pressure required to achieve desired CO2 volumes.
    """
    if not vol:
        vol = inputs.get_input("Desired volumes of CO2: ", lambda x: float(x))
    if not temp:
        temp = inputs.get_unit_input(ctx.obj["units"]["temp"],
                                     "Temperature of keg")

    if inputs.is_metric(ctx):
        temp = bm.c_to_f(temp)

    print("Keg pressure required: {0:.2f}psi".format(bm.keg_psi(temp, vol)))


@main.command()
@click.option(
    "-beer",
    type=float,
    help="Volume of beer to prime"
)
@click.option(
    "-vol",
    type=float,
    help="Volume of CO2 required"
)
@click.option(
    "-temp",
    type=float,
    help="Temperature of beer"
)
@click.pass_context
def prime(ctx, beer, vol, temp):
    """
    Calculates the amount of table sugar, corn sugar, or DME needed to achieve
    the requested CO2 volumes for bottle priming
    """
    if not beer:
        beer = inputs.get_unit_input(ctx.obj["units"]["vol"],
                                     "Volume of beer to prime")
    if not vol:
        vol = inputs.get_input("Desired volumes of CO2: ", lambda x: float(x))
    if not temp:
        temp = temp = inputs.get_unit_input(ctx.obj["units"]["temp"],
                                            "Temperature of beer")

    if inputs.is_metric(ctx):
        temp = bm.c_to_f(temp)
        beer = bm.l_to_g(beer)

    sugar = bm.priming(temp, beer, vol)
    if inputs.is_imperial(ctx):
        sugar = bm.g_to_oz(sugar)

    unit = ctx.obj["units"]["weight"]
    print()
    print("Use only one of the following:")
    print("Table sugar: {0:.2f}{1}".format(sugar, unit))
    print("Corn Sugar: {0:.2f}{1}".format(sugar * 1.099421965317919, unit))
    print("DME: {0:.2f}{1}".format(sugar * 1.4705202312138728, unit))


@main.command()
@click.option(
    "-temp",
    type=float,
    help="Current temperature of mash"
)
@click.option(
    "-target",
    type=float,
    help="Target temperature of mash"
)
@click.option(
    "-ratio",
    type=float,
    help="Grist/water ratio"
)
@click.option(
    "-grain",
    type=float,
    help="Weight of grain in mash"
)
@click.option(
    "-water",
    type=float,
    help="Temp of infusion water "
)
@click.pass_context
def infuse(ctx, temp, target, ratio, grain, water):
    """
    Given the current mash temperature, work out how much water of a given
    temp needs to be added to adjust the temperature
    """
    temp_unit = ctx.obj["units"]["temp"]
    if not temp:
        temp = temp = inputs.get_unit_input(temp_unit,
                                            "Current temperature of mash")
    if not target:
        target = inputs.get_unit_input(temp_unit,
                                       "Target temperature of mash")
    if not ratio:
        unit = "Quarts/lbs"
        if inputs.is_metric(ctx):
            unit = "Liters/kg"
        ratio = inputs.get_unit_input(unit, "Grist/water ratio")
    if not grain:
        grain = inputs.get_unit_input(ctx.obj["units"]["lrg_weight"],
                                      "Weight of grain in mash")
    if not water:
        water = inputs.get_unit_input(ctx.obj["units"]["temp"],
                                      "Temperature of infusion water")
    try:
        infusion = bm.infusion(ratio, temp, target, water, grain)
    except ZeroDivisionError:
        infusion = 0

    unit = "quarts"
    if inputs.is_metric(ctx):
        unit = "liters"
    print("Infuse with {0:.2f} {1} @ {2}{3}"
          .format(infusion, unit, water, temp_unit))


@main.command()
@click.option(
    "-points",
    type=int,
    help=("Points needed to acheive target gravity "
          "(e.x. current gravity 1.045, target 1.050, points=5)")
)
@click.option(
    "-vol",
    type=float,
    help="Current volume of the wort"
)
@click.pass_context
def dme(ctx, points, vol):
    """
    Given the current volume of the mash, work out how much Dry Malt
    Extract(DME) to add to reach your target gravity
    """
    if not points:
        points = inputs.get_input("Points needed to achieve target gravity: ",
                                  lambda x: float(x))
    if not vol:
        vol = inputs.get_unit_input(ctx.obj["units"]["temp"],
                                    "Current volume of the wort")

    if inputs.is_metric(ctx):
        vol = bm.l_to_g(vol)

    amt_dme = bm.pre_boil_dme(points, vol)

    if inputs.is_metric(ctx):
        amt_dme = bm.oz_to_g(amt_dme)

    print("Add {0:.2f}{1} of DME to raise the wort gravity by {2} points"
          .format(amt_dme, ctx.obj["units"]["weight"], points))


@main.command()
@click.option(
    "-og",
    type=float,
    help="Original Gravity as value between 1.000 and 1.200"
)
@click.option(
    "-fg",
    type=float,
    help="Final/current Gravity as value between 1.000 and 1.200"
)
@click.pass_context
def attenuation(ctx, og, fg):
    """
    Calculates the apparent and real attenuation from the provided
    original and final/current gravity.
    Real attenuation is the adjusted value taking into account the
    alcohol in the beer
    """
    if not og:
        og = inputs.get_gravity_input(ctx, "Original Gravity: ")
    if not fg:
        fg = inputs.get_gravity_input(ctx, "Current Gravity: ")

    # If passed in via options we need to check valid range
    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og) or not valid_range(fg):
        sys.exit(1)

    if fg > og:
        print("Final gravity cannot be higher than original gravity")
        sys.exit(1)

    print("Apparent attenuation: {0:.2f}%"
          .format(bm.apparent_attenuation(og, fg) * 100))
    print("Real attenuation: {0:.2f}%"
          .format(bm.real_attenuation(og, fg) * 100))


@main.command()
@click.option(
    "-og",
    type=float,
    help="Original Gravity as value between 1.000 and 1.200"
)
@click.option(
    "-att",
    type=float,
    help="Desired attenuation in %"
)
@click.pass_context
def fg_from_att(ctx, og, att):
    """
    Given a starting gravity and a desired attenuation level, will
    return the specific gravity for that percentage of attenuation.
    Useful if you have to action something at a given attenuation point
    and need to know what the gravity is when that point is reached
    """
    if not og:
        og = inputs.get_gravity_input(ctx, "Original Gravity: ")
    if not att:
        att = inputs.get_input("Desired attenuation in %: ",
                               lambda x: float(x))

    # If passed in via options we need to check valid range
    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og):
        sys.exit(1)

    print("FG for {0}% attenuation: {1:.3f}"
          .format(att, bm.fg_from_attenuation(og, att)))


@main.command()
@click.option(
    "-og",
    type=float,
    help="Current Gravity as value between 1.000 and 1.200"
)
@click.option(
    "-vol",
    type=float,
    help="Current wort volume"
)
@click.option(
    "-ng",
    type=float,
    help="The desired gravity as a value between 1.000 and 1.200"
)
@click.pass_context
def adjust_gravity(ctx, og, vol, ng):
    """
    Calculate the amount of liquid to boil off/dilute with
    to achieve a desired gravity.
    """
    if not og:
        og = inputs.get_gravity_input(ctx, "Original Gravity: ")
    if not ng:
        ng = inputs.get_gravity_input(ctx, "Desired Gravity: ")
    if not vol:
        vol = inputs.get_unit_input(ctx.obj["units"]["vol"],
                                    "Current volume of wort")

    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og) or not valid_range(ng):
        sys.exit(1)

    vol_adj = bm.adjust_gravity_volume(vol, og, ng)
    print("\nNew volume of wort will be {0:.2f}".format(vol_adj))
    diff = vol - vol_adj
    if diff >= 0:
        print("Boil off {0:.2f} {1} of wort".format(diff,
                                                    ctx.obj["units"]["vol"]))
    else:
        print("Dilute wort with {0:.2f} {1} of water"
              .format(diff * -1, ctx.obj["units"]["vol"]))


@main.command()
@click.option(
    "-og",
    type=float,
    help="Current Gravity as value between 1.000 and 1.200"
)
@click.option(
    "-vol",
    type=float,
    help="Current wort volume"
)
@click.option(
    "-newvol",
    type=float,
    help="The new wort volume"
)
@click.pass_context
def adjust_volume(ctx, og, vol, newvol):
    """
    Calculate the new gravity after a change in wort volume either through
    dilution or boil off
    """
    if not og:
        og = inputs.get_gravity_input(ctx, "Original Gravity: ")
    if not vol:
        vol = inputs.get_unit_input(ctx.obj["units"]["vol"],
                                    "Current volume of wort")
    if not newvol:
        newvol = inputs.get_unit_input(ctx.obj["units"]["vol"],
                                       "New volume of wort")

    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og):
        sys.exit(1)

    new_grav = bm.adjust_volume_gravity(vol, og, newvol)
    print("The new gravity will be {0:.3f}".format(new_grav))


def run():
    main()


if __name__ == "__main__":
    run()
