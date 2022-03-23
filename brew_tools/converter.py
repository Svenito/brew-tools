import brew_tools.brew_maths as bm


def print_mass(value: float) -> None:
    print("{0} kg => {1:.3f} lbs".format(value, bm.kg_to_lbs(value)))
    print("{0} g => {1:.3f} oz".format(value, bm.g_to_oz(value)))
    print("{0} lbs => {1:.3f} kg".format(value, bm.lbs_to_kg(value)))
    print("{0} oz => {1:.3f} g".format(value, bm.oz_to_g(value)))


def print_volume(value: float) -> None:
    print("{0} l => {1:.3f} gal".format(value, bm.l_to_g(value)))
    print("{0} gal => {1:.3f} l".format(value, bm.g_to_l(value)))


def print_gravity(value: float) -> None:
    print("{0} SG => {1:.3f} Plato".format(value, bm.to_plato(value)))
    print("{0} Plato => {1:.3f} SG".format(value, bm.to_sg(value)))


def print_colour(value: float) -> None:
    print(
        "{0} L => {1:.3f} EBC => {2:.3f} SRM".format(
            value, bm.l_to_ebc(value), bm.l_to_srm(value)
        )
    )
    print(
        "{0} EBC => {1:.3f} L => {2:.3f} SRM".format(
            value, bm.ebc_to_l(value), bm.ebc_to_srm(value)
        )
    )
    print(
        "{0} SRM => {1:.3f} EBC => {2:.3f} L".format(
            value, bm.srm_to_ebc(value), bm.srm_to_l(value)
        )
    )
