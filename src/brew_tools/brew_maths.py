import math


def oz_to_g(oz):
    return oz * 28.34952


def g_to_oz(g):
    return g / 28.34952


def c_to_f(c):
    return c * 1.8 + 32.0


def f_to_c(f):
    return f / 1.8 - 32.0


def l_to_g(l):
    return l * 0.26417


def to_brix(value):
    """
    Convert gravity value to brix value
    """
    brix = (((182.4601 * value - 775.6821) *
            value + 1262.7794) * value - 669.5622)
    return brix


def adjust_gravity(og, fg):
    """
    Adjust final gravity for wort correction and alcohol
    """
    adjusted_fg = (1.0000 - 0.00085683 * to_brix(og)) + 0.0034941 * to_brix(fg)
    return adjusted_fg


def keg_psi(temp, co2):
    # From http://www.wetnewf.org/pdfs/Brewing_articles/CO2%20Volumes.pdf
    # V = (P + 14.695) * ( 0.01821 + 0.09011*EXP(-(T-32)/43.11) ) - 0.003342

    henry_coeff = 0.01821 + 0.09011 * math.exp(-(temp-32)/43.11)
    pressure = ((co2 + 0.003342) / henry_coeff) - 14.695
    return pressure


def priming(temp, beer_vol, co2):
    # http://www.straighttothepint.com/priming-sugar-calculator/
    # PS = 15.195 × Vbeer × (VCO2 – 3.0378 + (0.050062 × Tferm) –
    # (0.00026555 × (Tferm ^ 2))
    return (15.195 * beer_vol *
            (co2 - 3.0378 + (0.050062 * temp) -
             (0.00026555 * (temp ** 2))))
