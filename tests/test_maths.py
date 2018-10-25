import pytest

from brew_tools import brew_maths as bm


def test_oz_to_g():
    g = bm.oz_to_g(34)
    assert g == pytest.approx(963.883, 0.001)


def test_g_to_oz():
    oz = bm.g_to_oz(34)
    assert oz == pytest.approx(1.199, 0.001)


def test_to_brix():
    brix = bm.to_brix(1.045)
    assert brix == pytest.approx(11.195, 0.001)


