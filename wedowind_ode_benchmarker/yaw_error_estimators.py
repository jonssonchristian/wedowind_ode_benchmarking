"""Module for yaw error estimator implementations."""

import pandas as pd

from wedowind_ode_benchmarker import registry


@registry.register_yaw_error_estimator
def curve_fit_yaw_error(
    time_series: pd.DataFrame,
    turbine_number: int,
    wind_speed_estimate: pd.Series,
) -> pd.Series:
    print(time_series.shape)
    print(turbine_number)

    return wind_speed_estimate
