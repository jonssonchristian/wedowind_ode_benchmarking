"""Functionality to collect benchmark data."""

from typing import Final
from pathlib import Path
import zipfile

import requests

from wedowind_ode_benchmarker.benchmark_datasets import DATASETS, DatasetSpecification
from wedowind_ode_benchmarker import benchmark_datasets

MB_CHUNK_SIZE: Final[int] = 1024 * 1024


def download_file(
    url: str,
    output_filepath: Path,
) -> None:
    """Download a data file from a URL.

    The download process may fail due to an SSL certification error. If
    that occurs, it is necessary to specify the path to the certificate
    for the Zenodo website in the ``verify`` argument when calling
    ``requests.get()``.

    :param url: the URL of the benchmark data file
    :param output_filepath: the filepath to which to save the benchmark
        data file
    """
    with output_filepath.open("wb") as f:
        for chunk in requests.get(
            url,
            stream=True,
        ).iter_content(
            chunk_size=MB_CHUNK_SIZE,
        ):
            f.write(chunk)


def collect_file(
    filename: str,
    zenodo_record_url: str,
    output_dirpath: Path,
) -> None:
    """Collect a file from a Zenodo URL, if it does not exist.

    If the file is a ZIP archive, the files within the archive are also
    extracted and the archive file deleted.

    :param filename: the name of the benchmark data file to download
    :param zenodo_record_url: the zenodo record URL corresponding to the
        benchmark dataset that the file is part of
    :param output_dirpath: the path of the directory to which to save
        the benchmark data files
    """
    output_filepath = output_dirpath / filename
    if output_filepath.is_file():
        return

    download_file(
        url=benchmark_datasets.get_zenodo_file_url(
            filename=filename,
            zenodo_record_url=zenodo_record_url,
        ),
        output_filepath=output_filepath,
    )

    if output_filepath.suffix.lower() != ".zip":
        return

    with zipfile.ZipFile(output_filepath, "r") as zip_ref:
        zip_ref.extractall(output_dirpath)

    output_filepath.unlink()


def collect_dataset(
    dataset_specification: DatasetSpecification,
    output_dirpath: Path,
) -> None:
    """Collect all files for a benchmark dataset.

    :param dataset_specification: the specifications of the benchmark
        dataset for which to collect data
    :param output_dirpath: the path of the directory to which to save
        the benchmark data files
    """
    collect_file(
        filename=dataset_specification.kmz_filename,
        zenodo_record_url=dataset_specification.zenodo_record_url,
        output_dirpath=output_dirpath,
    )

    for scada_archive_filename in dataset_specification.scada_archive_filenames:
        collect_file(
            filename=scada_archive_filename,
            zenodo_record_url=dataset_specification.zenodo_record_url,
            output_dirpath=output_dirpath,
        )


def collect_all_data(output_dirpath: Path) -> None:
    """Collect all benchmark data.

    :param output_dirpath: the path of the directory to which to save
        the benchmark data files
    """
    output_dirpath.mkdir(parents=True, exist_ok=True)
    for dataset_specification in DATASETS:
        collect_dataset(
            dataset_specification=dataset_specification,
            output_dirpath=output_dirpath,
        )
