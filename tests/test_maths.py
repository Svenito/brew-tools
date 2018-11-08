import pytest

from brew_tools import brew_maths as bm


def test_oz_to_g():
    g = bm.oz_to_g(34)
    assert g == pytest.approx(963.883, 0.001)


def test_g_to_oz():
    oz = bm.g_to_oz(34)
    assert oz == pytest.approx(1.199, 0.001)


def test_lbs_to_oz():
    oz = bm.lbs_to_oz(2)
    assert oz == pytest.approx(32, 0.01)


def test_c_to_f():
    f = bm.c_to_f(28)
    assert f == pytest.approx(82.4, 0.1)


def test_f_to_c():
    c = bm.f_to_c(82.4)
    assert c == pytest.approx(28, 0.1)


def test_l_to_g():
    g = bm.l_to_g(47)
    assert g == pytest.approx(12.416, 0.001)


def test_g_to_l():
    l = bm.g_to_l(12.41)
    assert l == pytest.approx(47, 0.1)


def test_l_to_q():
    q = bm.l_to_q(12)
    assert q == pytest.approx(12.68, 0.001)


def test_kg_to_lbs():
    lbs = bm.kg_to_lbs(5.4)
    assert lbs == pytest.approx(11.904, 0.001)


def test_to_brix():
    brix = bm.to_brix(1.045)
    assert brix == pytest.approx(11.195, 0.001)


def test_adjust_gravity():
    adjusted = bm.adjust_gravity(1.075, 1.022)
    assert adjusted == pytest.approx(1.004, 0.001)


def test_priming():
    prim_amount = bm.priming(68, 5, 2)
    assert prim_amount == pytest.approx(86.498, 0.001)


def test_infusion():
    infuse_water = bm.infusion(1.5, 152, 168, 212, 10)
    assert infuse_water == pytest.approx(6.1818, 0.001)


def test_abv():
    abv = bm.abv(1.04, 1.01)
    assert abv == pytest.approx(5.199, 0.001)


def test_pre_boil_dme():
    dme = bm.pre_boil_dme(5, 3.25)
    assert dme == pytest.approx(5.91, 0.01)


def test_apparent_attenuation():
    aa = bm.apparent_attenuation(1.032, 1.015)
    assert aa == pytest.approx(0.5246, 0.001)


def test_real_attenuation():
    aa = bm.real_attenuation(1.032, 1.015)
    assert aa == pytest.approx(0.4298, 0.001)


def test_fg_from_attenuation():
    fg = bm.fg_from_attenuation(1.04, 49)
    assert fg == pytest.approx(1.02, 0.001)


def test_adjust_gravity_volume():
    new_vol = bm.adjust_gravity_volume(4, 1.04, 1.07)
    assert new_vol == pytest.approx(2.29, 0.01)

    new_vol = bm.adjust_gravity_volume(7, 1.06, 1.04)
    assert new_vol == pytest.approx(10.50, 0.01)


def test_adjust_volume_gravity():
    new_grav = bm.adjust_volume_gravity(5, 1.04, 3)
    assert new_grav == pytest.approx(1.067, 0.001)