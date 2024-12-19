"""Module for data filterer implementations."""

import pandas as pd

from wedowind_ode_benchmarker.variables import PITCH_ANGLE_LABEL
from wedowind_ode_benchmarker import registry


@registry.register_data_filterer
def apply_basic_pitch_angle_filter(time_series: pd.DataFrame) -> pd.DataFrame:
    """Apply simple filter by pitch angle range.

    Keep data only in the pitch angle range from -1.5 degrees to 1.5
    degrees.
    """
    return time_series[
        (time_series[PITCH_ANGLE_LABEL] > -1.5) & (time_series[PITCH_ANGLE_LABEL] < 1.5)
    ]
