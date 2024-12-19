"""Module for wind speed estimator implementations."""

import pandas as pd

from wedowind_ode_benchmarker import registry
from wedowind_ode_benchmarker.variables import (
    WIND_SPEED_LABEL,
    TURBINE_NUMBER_LABEL,
    DATETIME_LABEL,
)


@registry.register_wind_speed_estimator
def use_turbine_wind_speed(
    time_series: pd.DataFrame,
    turbine_number: int,
) -> pd.Series:
    """Use the wind speed signal from the turbine being assessed."""
    return time_series.loc[
        time_series[TURBINE_NUMBER_LABEL] == turbine_number,
        :,
    ][WIND_SPEED_LABEL]


@registry.register_wind_speed_estimator
def use_mean_other_turbine_wind_speed(
    time_series: pd.DataFrame,
    turbine_number: int,
) -> pd.Series:
    """Use the mean wind speed across the other turbines."""
    return (
        time_series.loc[time_series[TURBINE_NUMBER_LABEL] != turbine_number, :]
        .groupby(DATETIME_LABEL)[WIND_SPEED_LABEL]
        .mean()
    )
