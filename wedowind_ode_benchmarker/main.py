"""Main interface for the WeDoWind ODE benchmarker."""

import logging

from wedowind_ode_benchmarker import benchmark_runner


def main() -> None:
    _setup_logging()
    benchmark_runner.run()


def _setup_logging() -> None:
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])


if __name__ == "__main__":
    main()
