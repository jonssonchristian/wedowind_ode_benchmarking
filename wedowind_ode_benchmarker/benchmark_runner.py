"""Functionality to run the benchmark."""

import logging

from pathlib import Path

from wedowind_ode_benchmarker import benchmark_data_collector, benchmark_data_parser


def run() -> None:
    """Run the complete benchmark."""
    logging.info("Starting the WeDoWind ODE benchmark process.")

    benchmark_data_collector.collect_all_data(output_dirpath=Path() / "data")

    for wind_farm_name in benchmark_data_parser.get_wind_farm_names():
        run_wind_farm(wind_farm_name=wind_farm_name)


def run_wind_farm(wind_farm_name: str) -> None:
    logging.info(
        f"Starting processing of the benchmark for the wind farm '{wind_farm_name}'."
    )

    time_series = benchmark_data_parser.parse_wind_farm_data(
        wind_farm_name=wind_farm_name,
    )
    print(time_series)
