
from glider_utils import (
    validate_glider_dataset,
)

from gsw.gibbs.conversions import SA_from_SP, CT_from_t
from gsw.gibbs.density_enthalpy_48 import rho

COND_DIM = 1
TEMP_DIM = 2
PRES_DIM = 3
SALI_DIM = 4
LAT_DIM = 5
LON_DIM = 6
SA_DIM = 7
CT_DIM = 8
DEN_DIM = 9

import numpy as np


def calculate_density(salinity_dataset, latitude, longitude):
    """Calculates density given glider practical salinity, pressure, latitude,
    and longitude using Gibbs gsw SA_from_SP and rho functions.

    Parameters:
        'salinity_dataset': An N x 5 array of timestamps (UNIX epoch),
              conductivity (mS/cm), temperature (C), pressure (dbar) and
              salinity (psu PSS-78).
        'latitude': An N dimensional array of latitude values
        'longitude': An N dimensional array of longitude values

    Returns:
        'density_dataset': An N x 10 array of timestamps, conductivity(mS/cm),
            temperature (C), pressure (dbar), salinity (psu PSS-78), latitude,
            longitude, absolute salinity(g/kg), conservative temperature (C)
            and density (kg/m**3)
    """

    density_dataset = np.zeros((len(salinity_dataset), 10))
    for i in range(0, 5):
        density_dataset[:, i] = salinity_dataset[:, i]

    density_dataset[:, LAT_DIM] = latitude
    density_dataset[:, LON_DIM] = longitude

    density_dataset = validate_glider_dataset(density_dataset)

    density_dataset[:, SA_DIM] = SA_from_SP(
        density_dataset[:, SALI_DIM],
        density_dataset[:, PRES_DIM],
        density_dataset[:, LON_DIM],
        density_dataset[:, LAT_DIM]
    )

    density_dataset[:, CT_DIM] = CT_from_t(
        density_dataset[:, SA_DIM],
        density_dataset[:, TEMP_DIM],
        density_dataset[:, PRES_DIM]
    )

    density_dataset[:, DEN_DIM] = rho(
        density_dataset[:, SA_DIM],
        density_dataset[:, CT_DIM],
        density_dataset[:, PRES_DIM]
    )

    return density_dataset