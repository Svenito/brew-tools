import click

import sys
import logging

from brew_tools import __version__
from brew_tools import inputs
from brew_tools import config
import brew_tools.brew_maths as bm
import brew_tools.converter as converter

__author__ = "Sven Steinbauer"
__copyright__ = "Sven Steinbauer"
__license__ = "mit"

_logger = logging.getLogger(__name__)


UNITS = {
    "metric": {"temp": "C", "weight": "g", "lrg_weight": "kg", "vol": "liter"},
    "imperial": {"temp": "F", "weight": "oz", "lrg_weight": "lbs", "vol": "US Gal"},
}


def is_metric(ctx):
    """
    Returns if the current context is in metric.

    :arg ctx: Current Click context
    :return: true if it is in metric, false otherwise
    """
    return ctx.obj["unit"] == "metric"


def is_imperial(ctx):
    """
    Returns if the current context is in imperial.

    :arg ctx: Current Click context
    :return: true if it is in imperial, false otherwise
    """
    return not is_metric(ctx)


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--unit",
    help="Ignore config and use a different unit.",
    type=click.Choice(["metric", "imperial"]),
    required=False,
)
@click.pass_context
def main(ctx, unit):
    """
    Brew-Tools is a small commandline utility that offers quick access to a
    set of calculators and tools to help homebrewers create their brews.

    All values and calculations are provided as guidelines only.
    Brew-tools should not be used for professional brewing. No warranty
    or guarantee of accuracy is provided on the information provided by
    this calculator.
    """
    ctx.ensure_object(dict)

    if not unit:
        try:
            unit = config.current_config["general"]["unit"]
        except KeyError:
            # Fallback to metric if all else fails
            print(
                f"Error with config file {config.config_file()}. Defaulting to metric."
            )
            unit = "metric"

    ctx.obj["units"] = UNITS[unit]
    ctx.obj["unit"] = unit


@main.command()
@click.option(
    "-og", type=float, help="Original Gravity as value between 1.000 and 1.200"
)
@click.option("-fg", type=float, help="Final Gravity as value between 1.000 and 1.200")
@click.option(
    "-adjust",
    is_flag=True,
    help=(
        "Apply wort and alcohol correction factor to "
        "final gravity if not using a refractometer. "
        "Default is to not apply it."
    ),
    default=False,
)
@click.pass_context
def abv(ctx, og, fg, adjust):
    """
    Calculates the ABV from the original and final gravity readings. By default
    the wort and alcohol correction factor is not applied. If you are using a
    hydrometer add the ``adjust`` flag to automatically correct the final
    gravity.
    """
    # These prompts are used instead of using the `prompt` attribute in the
    # click options so that it is possible to add units to the end of the
    # prompt based on the requested unit format.
    if not og:
        og = inputs.get_gravity_input("Original Gravity: ")
    if not fg:
        fg = inputs.get_gravity_input("Final Gravity: ")

    # If passed in via options we need to check valid range
    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og) or not valid_range(fg):
        sys.exit(1)

    if fg > og:
        print("Final gravity cannot be higher than original gravity")
        sys.exit(1)

    print("Estimated ABV: {0:.2f}%".format(bm.abv(og, fg, adjust)))


@main.command()
@click.option("-vol", type=float, help="Desired volumes of CO2")
@click.option("-temp", type=float, help="Temperature of keg")
@click.pass_context
def kegpsi(ctx, vol, temp):
    """
    Calculates the regulator pressure required to achieve desired CO2 volumes.
    """
    if not vol:
        vol = inputs.get_input("Desired volumes of CO2: ", lambda x: float(x))
    if not temp:
        temp = inputs.get_unit_input(ctx.obj["units"]["temp"], "Temperature of keg")

    if is_metric(ctx):
        temp = bm.c_to_f(temp)

    print("Keg pressure required: {0:.2f}psi".format(bm.keg_psi(temp, vol)))


@main.command()
@click.option("-beer", type=float, help="Volume of beer to prime")
@click.option("-vol", type=float, help="Volume of CO2 required")
@click.option("-temp", type=float, help="Temperature of beer")
@click.pass_context
def prime(ctx, beer, vol, temp):
    """
    Calculates the amount of table sugar, corn sugar, or DME needed to achieve
    the requested CO2 volumes for bottle priming
    """
    if not beer:
        beer = inputs.get_unit_input(ctx.obj["units"]["vol"], "Volume of beer to prime")
    if not vol:
        vol = inputs.get_input("Desired volumes of CO2: ", lambda x: float(x))
    if not temp:
        temp = temp = inputs.get_unit_input(
            ctx.obj["units"]["temp"], "Temperature of beer"
        )

    if is_metric(ctx):
        temp = bm.c_to_f(temp)
        beer = bm.l_to_g(beer)

    sugar = bm.priming(temp, beer, vol)
    if is_imperial(ctx):
        sugar = bm.g_to_oz(sugar)

    unit = ctx.obj["units"]["weight"]
    print()
    print("Use only one of the following:")
    print("Table sugar: {0:.2f}{1}".format(sugar, unit))
    print("Corn Sugar: {0:.2f}{1}".format(sugar * 1.099421965317919, unit))
    print("DME: {0:.2f}{1}".format(sugar * 1.4705202312138728, unit))


@main.command()
@click.option("-temp", type=float, help="Current temperature of mash")
@click.option("-target", type=float, help="Target temperature of mash")
@click.option("-ratio", type=float, help="Grist/water ratio")
@click.option("-grain", type=float, help="Weight of grain in mash")
@click.option("-water", type=float, help="Temp of infusion water ")
@click.pass_context
def infuse(ctx, temp, target, ratio, grain, water):
    """
    Given the current mash temperature, work out how much water of a given
    temp needs to be added to adjust the temperature
    """
    temp_unit = ctx.obj["units"]["temp"]
    if not temp:
        temp = temp = inputs.get_unit_input(temp_unit, "Current temperature of mash")
    if not target:
        target = inputs.get_unit_input(temp_unit, "Target temperature of mash")
    if not ratio:
        unit = "Quarts/lbs"
        if is_metric(ctx):
            unit = "Liters/kg"
        ratio = inputs.get_unit_input(unit, "Grist/water ratio")
    if not grain:
        grain = inputs.get_unit_input(
            ctx.obj["units"]["lrg_weight"], "Weight of grain in mash"
        )
    if not water:
        water = inputs.get_unit_input(
            ctx.obj["units"]["temp"], "Temperature of infusion water"
        )
    try:
        infusion = bm.infusion(ratio, temp, target, water, grain)
    except ZeroDivisionError:
        infusion = 0

    unit = "quarts"
    if is_metric(ctx):
        unit = "liters"
    print("Infuse with {0:.2f} {1} @ {2}{3}".format(infusion, unit, water, temp_unit))


@main.command()
@click.option(
    "-points",
    type=int,
    help=(
        "Points needed to acheive target gravity "
        "(e.x. current gravity 1.045, target 1.050, points=5)"
    ),
)
@click.option("-vol", type=float, help="Current volume of the wort")
@click.pass_context
def dme(ctx, points, vol):
    """
    Given the current volume of the mash, work out how much Dry Malt
    Extract(DME) to add to reach your target gravity
    """
    if not points:
        points = inputs.get_input(
            "Points needed to achieve target gravity: ", lambda x: float(x)
        )
    if not vol:
        vol = inputs.get_unit_input(
            ctx.obj["units"]["temp"], "Current volume of the wort"
        )

    if is_metric(ctx):
        vol = bm.l_to_g(vol)

    amt_dme = bm.pre_boil_dme(points, vol)

    if is_metric(ctx):
        amt_dme = bm.oz_to_g(amt_dme)

    print(
        "Add {0:.2f}{1} of DME to raise the wort gravity by {2} points".format(
            amt_dme, ctx.obj["units"]["weight"], points
        )
    )


@main.command()
@click.option(
    "-og", type=float, help="Original Gravity as value between 1.000 and 1.200"
)
@click.option(
    "-fg", type=float, help="Final/current Gravity as value between 1.000 and 1.200"
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
        og = inputs.get_gravity_input("Original Gravity: ")
    if not fg:
        fg = inputs.get_gravity_input("Current Gravity: ")

    # If passed in via options we need to check valid range
    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og) or not valid_range(fg):
        sys.exit(1)

    if fg > og:
        print("Final gravity cannot be higher than original gravity")
        sys.exit(1)

    print(
        "Apparent attenuation: {0:.2f}%".format(bm.apparent_attenuation(og, fg) * 100)
    )
    print("Real attenuation: {0:.2f}%".format(bm.real_attenuation(og, fg) * 100))


@main.command()
@click.option(
    "-og", type=float, help="Original Gravity as value between 1.000 and 1.200"
)
@click.option("-att", type=float, help="Desired attenuation in %")
@click.pass_context
def fg_from_att(ctx, og, att):
    """
    Given a starting gravity and a desired attenuation level, will
    return the specific gravity for that percentage of attenuation.
    Useful if you have to action something at a given attenuation point
    and need to know what the gravity is when that point is reached
    """
    if not og:
        og = inputs.get_gravity_input("Original Gravity: ")
    if not att:
        att = inputs.get_input("Desired attenuation in %: ", lambda x: float(x))

    # If passed in via options we need to check valid range
    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og):
        sys.exit(1)

    print(
        "FG for {0}% attenuation: {1:.3f}".format(att, bm.fg_from_attenuation(og, att))
    )


@main.command()
@click.option(
    "-og", type=float, help="Current Gravity as value between 1.000 and 1.200"
)
@click.option("-vol", type=float, help="Current wort volume")
@click.option(
    "-ng", type=float, help="The desired gravity as a value between 1.000 and 1.200"
)
@click.pass_context
def adjust_gravity(ctx, og, vol, ng):
    """
    Calculate the amount of liquid to boil off/dilute with
    to achieve a desired gravity.
    """
    if not og:
        og = inputs.get_gravity_input("Original Gravity: ")
    if not ng:
        ng = inputs.get_gravity_input("Desired Gravity: ")
    if not vol:
        vol = inputs.get_unit_input(ctx.obj["units"]["vol"], "Current volume of wort")

    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og) or not valid_range(ng):
        sys.exit(1)

    vol_adj = bm.adjust_gravity_volume(vol, og, ng)
    print("\nNew volume of wort will be {0:.2f}".format(vol_adj))
    diff = vol - vol_adj
    if diff >= 0:
        print("Boil off {0:.2f} {1} of wort".format(diff, ctx.obj["units"]["vol"]))
    else:
        print(
            "Dilute wort with {0:.2f} {1} of water".format(
                diff * -1, ctx.obj["units"]["vol"]
            )
        )


@main.command()
@click.option(
    "-og", type=float, help="Current Gravity as value between 1.000 and 1.200"
)
@click.option("-vol", type=float, help="Current wort volume")
@click.option("-newvol", type=float, help="The new wort volume")
@click.pass_context
def adjust_volume(ctx, og, vol, newvol):
    """
    Calculate the new gravity after a change in wort volume either through
    dilution or boil off
    """
    if not og:
        og = inputs.get_gravity_input("Original Gravity: ")
    if not vol:
        vol = inputs.get_unit_input(ctx.obj["units"]["vol"], "Current volume of wort")
    if not newvol:
        newvol = inputs.get_unit_input(ctx.obj["units"]["vol"], "New volume of wort")

    valid_range = inputs.between(1.0, 1.2)
    if not valid_range(og):
        sys.exit(1)

    new_grav = bm.adjust_volume_gravity(vol, og, newvol)
    print("The new gravity will be {0:.3f}".format(new_grav))


@main.command()
@click.option("-grain", type=float, help="Weight of grain")
@click.option("-vol", type=float, help="Volume of water")
@click.option("-temp", type=float, help="Target mash temp")
@click.pass_context
def strike(ctx, grain, vol, temp):
    """
    Calculate the required strike water temperature given the mass of grains,
    volume of water, and desired final mash temperature
    """
    if not grain:
        grain = inputs.get_unit_input(
            ctx.obj["units"]["lrg_weight"], "Weight of grains: "
        )
    if not vol:
        vol = inputs.get_unit_input(ctx.obj["units"]["vol"], "Volume of water: ")
    if not temp:
        temp = inputs.get_unit_input(ctx.obj["units"]["temp"], "Desired mash temp: ")

    if is_metric(ctx):
        grain = bm.kg_to_lbs(grain)
        vol = bm.l_to_g(vol)
        temp = bm.c_to_f(temp)

    strike_temp = bm.strike_temp(grain, vol, temp)
    if is_metric(ctx):
        strike_temp = bm.f_to_c(strike_temp)

    print(
        "Strike water temp should be {0:.3f}{1}".format(
            strike_temp, ctx.obj["units"]["temp"]
        )
    )


@main.command()
@click.option("-sg", type=float, help="Measured gravity in SG")
@click.option("-temp", type=float, help="Temperature of measured wort")
@click.option("-caltemp", type=float, help="Calibration temp of hydrometer")
@click.pass_context
def adjust_sg(ctx, sg, temp, caltemp):
    """
    Calculate the adjusted single gravity according to the current temperature of the
    wort.
    """
    if not sg:
        sg = inputs.get_gravity_input("Original gravity: ")
    if not temp:
        temp = inputs.get_unit_input(ctx.obj["units"]["temp"], "Temp of wort: ")
    if not caltemp:
        caltemp = inputs.get_unit_input(ctx.obj["units"]["temp"], "Calibration temp: ")

    if is_metric(ctx):
        f_temp = bm.c_to_f(temp)
        f_caltemp = bm.c_to_f(caltemp)
        adjusted_grav = bm.gravity_temperature_correct(sg, f_temp, f_caltemp)
    else:
        adjusted_grav = bm.gravity_temperature_correct(sg, temp, caltemp)

    print(
        "Adjusted gravity at {0:.3f}{1} is: {2:.3f}".format(
            temp, ctx.obj["units"]["temp"], adjusted_grav
        )
    )


@main.command()
@click.argument(
    "what",
    type=click.Choice(["mass", "vol", "grav", "col"]),
)
@click.argument("value")
@click.pass_context
def convert(ctx, what, value):
    """
    Convert a value between given measurements. Supported types are:

    mass, vol, grav, col
    """
    value = float(value)
    if what == "mass":
        converter.print_mass(value)
    if what == "vol":
        converter.print_volume(value)
    if what == "grav":
        converter.print_gravity(value)
    if what == "col":
        converter.print_colour(value)


def run():
    if not config.exists():
        print("This is the first time you are running brew tools.")
        print("Please select your preferred units.")
        answer = inputs.get_choice("Enter selection:", config.units)

        config.current_config["general"] = {"unit": config.units[answer]}
        try:
            config.write_config()
        except Exception:
            # TODO allow user to ignore?
            print(
                f"Unable to write to f{config.config_file()}. Check permission and try again."
            )
            sys.exit(1)
    else:
        try:
            config.read_config()
        except Exception:
            print(f"Unable to read {config.config_file()}")
            sys.exit(1)
    main()


if __name__ == "__main__":
    run()
