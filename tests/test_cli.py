#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

__author__ = "Sven Steinbauer"
__copyright__ = "Sven Steinbauer"
__license__ = "mit"

from click.testing import CliRunner
from brew_tools import command_line


def test_abv():
    runner = CliRunner()
    result = runner.invoke(command_line.main, 'abv --og 1.05 --fg 1.02')

    assert result.exit_code == 0
    assert result.output == "Estimated ABV: 5.63%\n"


def test_abv_high_fg():
    runner = CliRunner()
    result = runner.invoke(command_line.main, 'abv --og 1.05 --fg 1.06')

    assert result.exit_code == 1
    assert result.output == "Final gravity cannot be higher than original gravity\n"


def test_abv_range():
    runner = CliRunner()
    result = runner.invoke(command_line.main, 'abv --og 2.0 --fg 1.06')
    assert result.exit_code == 1
    assert result.output == "ERROR: Value must be between 1.0 and 1.2\n"
