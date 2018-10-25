
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
    valid_range = utils.between(1.0, 1.2)
    if not og:
        og = utils.get_input("Original Gravity: ", lambda x: float(x),
                             valid_range)
    if not fg:
        fg = utils.get_input("Final Gravity: ", lambda x: float(x),
                             valid_range)

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
        unit = ctx.obj["units"]["vol"]
        beer = utils.get_input("Volume of beer to prime ({}): ".format(unit),
                               lambda x: float(x))
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


def run():
    main()


if __name__ == "__main__":
    run()
