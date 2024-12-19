"""Functionality to run the benchmark."""

import logging
from typing import Final
from pathlib import Path
from collections.abc import Sequence
import itertools

import pandas as pd

from wedowind_ode_benchmarker import (
    benchmark_data_collector,
    benchmark_data_parser,
    benchmark_data_processor,
    registry,
)
from wedowind_ode_benchmarker.variables import TURBINE_NUMBER_LABEL
from wedowind_ode_benchmarker.registry import (
    DataFiltererComponent,
    WindSpeedEstimatorComponent,
    YawErrorEstimatorComponent,
)


WIND_SPEED_BINS: Final[Sequence[float]] = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

YAW_ERROR_BINS: Final[Sequence[float]] = [float(x) for x in range(-25, 26, 1)]


def run() -> None:
    """Run the complete benchmark."""
    logging.info("Starting the WeDoWind ODE benchmark process.")

    benchmark_data_collector.collect_all_data(output_dirpath=Path() / "data")

    for (
        wind_farm_name,
        data_filterer,
        wind_speed_estimator,
        yaw_error_estimator,
    ) in itertools.product(
        benchmark_data_parser.get_wind_farm_names(),
        registry.get_data_filterers(),
        registry.get_wind_speed_estimators(),
        registry.get_yaw_error_estimators(),
    ):
        run_wind_farm_case(
            wind_farm_name=wind_farm_name,
            data_filterer=data_filterer,
            wind_speed_estimator=wind_speed_estimator,
            yaw_error_estimator=yaw_error_estimator,
        )


def run_wind_farm_case(
    wind_farm_name: str,
    data_filterer: DataFiltererComponent,
    wind_speed_estimator: WindSpeedEstimatorComponent,
    yaw_error_estimator: YawErrorEstimatorComponent,
) -> None:
    """Run a single benchmark case for a specific wind farm.

    :param wind_farm_name: the name of the wind farm for which to run
        the benchmark
    :param data_filterer: the wind speed filterer to use in the
        benchmark case execution
    :param wind_speed_estimator: the wind speed estimator to use in the
        benchmark case execution
    :param yaw_error_estimator: the yaw error estimator to use in the
        benchmark case execution
    """
    logging.info(
        f"Starting processing of the benchmark case for the wind farm "
        f"'{wind_farm_name}', using the data filterer function "
        f"'{data_filterer.get_name()}', the wind speed estimator "
        f"function '{wind_speed_estimator.get_name()}', and the yaw "
        f"error estimator function '{yaw_error_estimator.get_name()}'."
    )

    time_series = benchmark_data_parser.parse_wind_farm_data(
        wind_farm_name=wind_farm_name,
    )
    time_series = benchmark_data_processor.process(
        time_series=time_series,
    )
    time_series = data_filterer.function(time_series)

    for turbine_number in time_series[TURBINE_NUMBER_LABEL].unique():
        run_turbine_case(
            time_series=time_series,
            turbine_number=int(turbine_number),
            wind_speed_estimator=wind_speed_estimator,
            yaw_error_estimator=yaw_error_estimator,
        )


def run_turbine_case(
    time_series: pd.DataFrame,
    turbine_number: int,
    wind_speed_estimator: WindSpeedEstimatorComponent,
    yaw_error_estimator: YawErrorEstimatorComponent,
) -> None:
    """Run the benchmark for a turbine.

    :param time_series: the processed time series SCADA data including
        all turbines in the wind farm
    :param turbine_number: the number of the turbine for which to run
        the benchmark
    :param wind_speed_estimator: the wind speed estimator to use in the
        benchmark case execution
    :param yaw_error_estimator: the yaw error estimator to use in the
        benchmark case execution
    """
    wind_speed_estimate = wind_speed_estimator.function(
        time_series,
        turbine_number,
    )
    yaw_error_estimate = yaw_error_estimator.function(
        time_series,
        turbine_number,
        wind_speed_estimate,
    )
    print(yaw_error_estimate)
