
import click

import sys
import logging

from brew_tools import __version__
from brew_tools import utils
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
    if not og:
        og = utils.get_gravity_input("Original Gravity: ")
    if not fg:
        fg = utils.get_gravity_input("Final Gravity: ")

    valid_range = utils.between(1.0, 1.2)
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
        vol = utils.get_input("Desired volumes of CO2: ", lambda x: float(x))
    if not temp:
        unit = ctx.obj["units"]["temp"]
        temp = utils.get_input("Temperature of keg ({}): ".format(unit),
                               lambda x: float(x))

    if ctx.obj['unit'] == 'metric':
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
    the requested CO2 volumes
    """
    if not beer:
        beer = utils.get_vol_input(ctx, "Volume of beer to prime")
    if not vol:
        vol = utils.get_input("Desired volumes of CO2: ", lambda x: float(x))

    if not temp:
        unit = ctx.obj["units"]["temp"]
        temp = utils.get_input("Temperature of beer ({}): ".format(unit),
                               lambda x: float(x))

    if ctx.obj['unit'] == 'metric':
        temp = bm.c_to_f(temp)
        beer = bm.l_to_g(beer)

    sugar = bm.priming(temp, beer, vol)
    if ctx.obj['unit'] == 'imperial':
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
    if not temp:
        unit = ctx.obj["units"]["temp"]
        temp = utils.get_input("Current temperature of mash ({}): ".format(unit),
                               lambda x: float(x))
    if not target:
        unit = ctx.obj["units"]["temp"]
        target = utils.get_input("Target temperature of mash ({}): ".format(unit),
                                 lambda x: float(x))
    if not ratio:
        unit = "Quarts/lbs"
        if ctx.obj['unit'] == 'metric':
            unit = "Liters/kg"

        ratio = utils.get_input("Grist/water ratio: ({}) ".format(unit),
                                lambda x: float(x))
    if not grain:
        unit = ctx.obj["units"]["lrg_weight"]
        grain = utils.get_input("Weight of grain in mash ({}): ".format(unit),
                                lambda x: float(x))
    if not water:
        unit = ctx.obj["units"]["temp"]
        water = utils.get_input("Temperature of infusion water ({}): ".format(unit),
                                lambda x: float(x))
    try:
        infusion = bm.infusion(ratio, temp, target, water, grain)
    except ZeroDivisionError:
        infusion = 0

    unit = "quarts"
    if ctx.obj['unit'] == 'metric':
            unit = "liters"
    print("Infuse with {0:.2f} {1} @ {2}{3}"
          .format(infusion, unit,
                  water, ctx.obj["units"]["temp"]))


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
        points = utils.get_input("Points needed to achieve target gravity: ",
                                 lambda x: float(x))
    if not vol:
        vol = utils.get_vol_input(ctx, "Current volume of the wort")

    if ctx.obj['unit'] == 'metric':
        vol = bm.l_to_g(vol)

    amt_dme = bm.pre_boil_dme(points, vol)

    if ctx.obj['unit'] == 'metric':
        amt_dme = bm.oz_to_g(amt_dme)

    print("Add {0:.2f}{1} of DME to raise the wort gravity by {2} points"
          .format(amt_dme, ctx.obj["units"]["weight"], points))


def run():
    main()


if __name__ == "__main__":
    run()
