
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


@click.group()
@click.version_option(version=__version__)
@click.option(
    "-u",
    "--unit",
    help="Select units. Metric by default.",
    type=click.Choice(['metric', 'imperial']),
    default='metric'
)
@click.pass_context
def main(ctx, unit):
    ctx.ensure_object(dict)
    ctx.obj['units'] = unit


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
    if not og:
        og = utils.get_input("OG: ", lambda x: float(x),
                             utils.between(1.0, 1.2))
    if not fg:
        fg = utils.get_input("OG: ", lambda x: float(x),
                             utils.between(1.0, 1.2))
    if fg > og:
        print("Final gravity cannot be higher than original gravity")
        sys.exit(1)
    abv = (og - bm.adjust_gravity(og, fg)) * 131.25
    print(abv)


@main.command()
@click.option(
    "-vol",
    type=float,
    help="Desired volumes of CO2",
    prompt=True
)
@click.option(
    "-temp",
    type=float,
    help="Temperature of keg in F",
    prompt=True
)
@click.pass_context
def kegpsi(ctx, vol, temp):
    if ctx.obj['units'] == 'metric':
        temp = bm.c_to_f(temp)

    print(bm.keg_psi(temp, vol))


@main.command()
@click.option(
    "-beer",
    type=float,
    help="Volume of beer to prime (US Gal)",
    prompt=True
)
@click.option(
    "-co",
    type=float,
    help="Volume of CO2 required",
    prompt=True
)
@click.option(
    "-temp",
    type=float,
    help="Temperature of beer (F)",
    prompt=True
)
@click.pass_context
def prime(ctx, beer, co, temp):
    if ctx.obj['units'] == 'metric':
        temp = bm.c_to_f(temp)
        beer = bm.l_to_g(beer)

    sugar = bm.priming(temp, beer, co)
    print(sugar)
    print(sugar * 1.099421965317919)
    print(sugar * 1.4705202312138728)


def run():
    main()


if __name__ == "__main__":
    run()
