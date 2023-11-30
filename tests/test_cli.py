#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sven Steinbauer"
__copyright__ = "Sven Steinbauer"
__license__ = "mit"

import pytest
from click.testing import CliRunner

import brew_tools
from brew_tools import command_line


@pytest.fixture
def mock_config():
    def mock_ret(*args, **kwargs):
        return {"general": {"unit": "metric"}}

    return mock_ret


def mock_config_in_test(func):
    def inner(monkeypatch, mock_config, *args, **kwargs):
        monkeypatch.setattr(brew_tools.config, "current_config", mock_config())
        return func(*args, **kwargs)

    return inner


@mock_config_in_test
def test_abv():
    runner = CliRunner()
    result = runner.invoke(command_line.main, "abv -og 1.05 -fg 1.02 -adjust")
    print(result)
    assert result.exit_code == 0
    assert result.output == "Estimated ABV: 5.63%\n"


@mock_config_in_test
def test_abv_no_adjust():
    runner = CliRunner()
    result = runner.invoke(command_line.main, "abv -og 1.05 -fg 1.02 ")

    assert result.exit_code == 0
    assert result.output == "Estimated ABV: 3.94%\n"


@mock_config_in_test
def test_abv_high_fg():
    runner = CliRunner()
    result = runner.invoke(command_line.main, "abv -og 1.05 -fg 1.06")

    assert result.exit_code == 1
    assert result.output == (
        "Final gravity cannot be higher " "than original gravity\n"
    )


@mock_config_in_test
def test_abv_range():
    runner = CliRunner()
    result = runner.invoke(command_line.main, "abv -og 2.0 -fg 1.06")
    assert result.exit_code == 1
    assert result.output == "ERROR: Value must be between 1.0 and 1.2\n"


@mock_config_in_test
def test_kegpsi():
    runner = CliRunner()
    result = runner.invoke(command_line.main, "kegpsi -vol 2.0 -temp 15")
    assert result.exit_code == 0
    assert result.output == "Keg pressure required: 15.49psi\n"


@mock_config_in_test
def test_kegpsi_imp():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main, "--unit imperial kegpsi -vol 2.0 -temp 36"
    )
    assert result.exit_code == 0
    assert result.output == "Keg pressure required: 5.27psi\n"


@mock_config_in_test
def test_prime():
    runner = CliRunner()
    result = runner.invoke(command_line.main, "prime -beer 19 -vol 2.2 -temp 15")
    assert result.exit_code == 0
    assert result.output == (
        "\nUse only one of the following:\n"
        "Table sugar: 90.87g\n"
        "Corn Sugar: 99.91g\n"
        "DME: 133.63g\n"
    )


@mock_config_in_test
def test_prime_imperial():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main, "--unit imperial prime -beer 5 -vol 2.2 -temp 68"
    )
    assert result.exit_code == 0
    assert result.output == (
        "\nUse only one of the following:\n"
        "Table sugar: 3.59oz\n"
        "Corn Sugar: 3.94oz\n"
        "DME: 5.27oz\n"
    )


@mock_config_in_test
def test_infuse():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main,
        ("infuse -temp 66 -target 70 -ratio 1 " "-grain 5 -water 100"),
    )
    assert result.exit_code == 0
    assert result.output == "Infuse with 0.80 liters @ 100.0C\n"


@mock_config_in_test
def test_imperial():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main,
        (
            "--unit imperial infuse -temp 152 -target 168 "
            "-ratio 1.5 -grain 10 -water 212"
        ),
    )
    assert result.exit_code == 0
    assert result.output == "Infuse with 6.18 quarts @ 212.0F\n"


@mock_config_in_test
def test_dme():
    runner = CliRunner()
    result = runner.invoke(command_line.main, (" dme -points 5 -vol 12.3"))
    assert result.exit_code == 0
    assert result.output == "Add 167.48g of DME to raise the wort gravity by 5 points\n"


@mock_config_in_test
def test_dme_imperial():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main, ("--unit imperial dme -points 5 -vol 3.25")
    )
    assert result.exit_code == 0
    assert result.output == "Add 5.91oz of DME to raise the wort gravity by 5 points\n"


@mock_config_in_test
def test_attenuation():
    runner = CliRunner()
    result = runner.invoke(command_line.main, ("attenuation -og 1.06 -fg 1.023"))
    assert result.exit_code == 0
    assert result.output == (
        "Apparent attenuation: 60.46%\n" "Real attenuation: 49.53%\n"
    )


@mock_config_in_test
def test_fg_from_att():
    runner = CliRunner()
    result = runner.invoke(command_line.main, ("fg-from-att -og 1.04 -att 49"))
    assert result.exit_code == 0
    assert result.output == ("FG for 49.0% attenuation: 1.020\n")


@mock_config_in_test
def test_adj_grav_up_vol():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main, ("adjust-gravity -og 1.04 -ng 1.06 -vol 3")
    )
    assert result.exit_code == 0
    assert result.output == (
        "\nNew volume of wort will be 2.00\n" "Boil off 1.00 liter of wort\n"
    )


@mock_config_in_test
def test_adj_grav_down_vol():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main, ("adjust-gravity -og 1.05 -ng 1.04 -vol 5")
    )
    assert result.exit_code == 0
    assert result.output == (
        "\nNew volume of wort will be 6.25\n" "Dilute wort with 1.25 liter of water\n"
    )


@mock_config_in_test
def test_adj_vol():
    runner = CliRunner()
    result = runner.invoke(
        command_line.main, ("adjust-volume -og 1.05 -newvol 4 -vol 5")
    )
    assert result.exit_code == 0
    assert result.output == ("The new gravity will be 1.062\n")


@mock_config_in_test
def test_strike_temp():
    runner = CliRunner()
    result = runner.invoke(command_line.main, ("strike -grain 14 -vol 10 -temp 153"))
    assert result.exit_code == 0
    assert result.output == ("Strike water temp should be 232.688C\n")
