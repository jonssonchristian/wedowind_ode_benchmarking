"""Benchmark data processor module."""

import pandas as pd

from wedowind_ode_benchmarker.variables import (
    YAW_ERROR_LABEL,
    NACELLE_DIRECTION_LABEL,
    WIND_FROM_DIRECTION_LABEL,
)


def process(time_series: pd.DataFrame) -> pd.DataFrame:
    """Prepare the raw data for the benchmarking process.

    This function appends a column for yaw error, calculated as the
    circular difference between the nacelle direction and wind
    direction.

    :param time_series: the raw time series SCADA data
    """
    yaw_error = (
        time_series[NACELLE_DIRECTION_LABEL] - time_series[WIND_FROM_DIRECTION_LABEL]
    )
    yaw_error = (yaw_error + 180.0) % 360.0 - 180.0

    return time_series.assign(**{YAW_ERROR_LABEL: yaw_error})
