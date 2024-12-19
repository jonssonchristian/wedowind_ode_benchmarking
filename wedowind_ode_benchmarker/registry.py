"""Registry of methods for benchmarking."""

from typing import Callable, Literal
from dataclasses import dataclass
from collections.abc import Sequence

import pandas as pd


AssessmentComponentType = Literal[
    "data_filterer", "wind_speed_estimator", "yaw_error_estimator"
]


@dataclass
class DataFiltererComponent:
    """Specification of a data filterer assessment component."""

    function: Callable[[pd.DataFrame], pd.DataFrame]
    component_type: Literal["data_filterer"] = "data_filterer"

    def get_name(self) -> str:
        return self.function.__name__


@dataclass
class WindSpeedEstimatorComponent:
    """Specification of a wind speed estimator assessment component."""

    function: Callable[[pd.DataFrame, int], pd.Series]
    component_type: Literal["wind_speed_estimator"] = "wind_speed_estimator"

    def get_name(self) -> str:
        return self.function.__name__


@dataclass
class YawErrorEstimatorComponent:
    """Specification of a yaw error estimator assessment component."""

    function: Callable[[pd.DataFrame, int, pd.Series], pd.Series]
    component_type: Literal["yaw_error_estimator"] = "yaw_error_estimator"

    def get_name(self) -> str:
        return self.function.__name__


_data_filterers: list[DataFiltererComponent] = []
_wind_speed_estimators: list[WindSpeedEstimatorComponent] = []
_yaw_error_estimators: list[YawErrorEstimatorComponent] = []


def register_data_filterer(
    function: Callable[[pd.DataFrame], pd.DataFrame],
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    global _data_filterers
    _data_filterers.append(DataFiltererComponent(function=function))

    return function


def register_wind_speed_estimator(
    function: Callable[[pd.DataFrame, int], pd.Series],
) -> Callable[[pd.DataFrame, int], pd.Series]:
    _wind_speed_estimators.append(WindSpeedEstimatorComponent(function=function))

    return function


def register_yaw_error_estimator(
    function: Callable[[pd.DataFrame, int, pd.Series], pd.Series],
) -> Callable[[pd.DataFrame, int, pd.Series], pd.Series]:
    _yaw_error_estimators.append(YawErrorEstimatorComponent(function=function))

    return function


def get_data_filterers() -> Sequence[DataFiltererComponent]:
    """Get a sequence of all data filterers."""
    return _data_filterers


def get_wind_speed_estimators() -> Sequence[WindSpeedEstimatorComponent]:
    """Get a sequence of all wind speed estimators."""
    return _wind_speed_estimators


def get_yaw_error_estimators() -> Sequence[YawErrorEstimatorComponent]:
    """Get a sequence of all yaw error estimators."""
    return _yaw_error_estimators
