"""Parser module for the benchmark data."""

from pathlib import Path
from typing import Final
import re
from collections.abc import Iterable

import numpy as np
import pandas as pd


TURBINE_DATA_GLOB_PATTERN: Final[str] = "data/Turbine_Data*.csv"

SCADA_FILE_INDEX_COLUMN: Final[str] = "# Date and time"

SCADA_FILE_SELECTED_COLUMNS: Final[list[str]] = [
    "# Date and time",
    "Power (kW)",
    "Wind speed (m/s)",
    "Wind direction (°)",
    "Nacelle position (°)",
    "Blade angle (pitch position) A (°)",
]

TURBINE_DETAILS_FROM_FILE_PATTERN: Final[re.Pattern] = re.compile(
    pattern=r"^Turbine_Data_(\w+)_(\d+)_.*\.csv$",
    flags=re.ASCII,
)


def get_wind_farm_names() -> Iterable[str]:
    """Get the names of the wind farms for which data is available."""
    return set(
        _get_wind_farm_name(filepath=filepath)
        for filepath in Path().rglob(TURBINE_DATA_GLOB_PATTERN)
    )


def parse_wind_farm_data(wind_farm_name: str) -> pd.DataFrame:
    """Parse the time series data for a wind farm.

    :param wind_farm_name: the name of the wind farm for which to parse
        time series data
    """
    time_series_list: list[pd.DataFrame] = []
    for filepath in Path().rglob(TURBINE_DATA_GLOB_PATTERN):
        if _get_wind_farm_name(filepath=filepath) != wind_farm_name:
            continue

        turbine_number = _get_turbine_number(filepath=filepath)

        time_series = (
            pd.read_csv(
                filepath,
                index_col=SCADA_FILE_INDEX_COLUMN,
                parse_dates=True,
                skiprows=9,
                usecols=SCADA_FILE_SELECTED_COLUMNS,
                dtype=np.float64,
            )
            .assign(
                turbine_number=turbine_number,
            )
            .rename_axis(
                index="datetime",
            )
        )

        time_series_list.append(time_series)

    return pd.concat(time_series_list, axis="index", join="outer")


def _get_turbine_details_match(filepath: Path) -> re.Match[str]:
    match = TURBINE_DETAILS_FROM_FILE_PATTERN.match(string=filepath.name)

    if match is None:
        raise ValueError(
            f"Failed to match turbine details for the filename '{filepath.name}'."
        )

    return match


def _get_wind_farm_name(filepath: Path) -> str:
    return _get_turbine_details_match(filepath=filepath).group(1)


def _get_turbine_number(filepath: Path) -> int:
    return int(_get_turbine_details_match(filepath=filepath).group(2))
