"""Specification of benchmark datasets."""

from dataclasses import dataclass
from typing import Final, Sequence, TypeAlias


SiteName: TypeAlias = str


@dataclass
class DatasetSpecification:
    site_name: str
    zenodo_record_url: str
    kmz_filename: str
    scada_archive_filenames: Sequence[str]


# Initially, only a subset of the SCADA data files are included
DATASETS: Final[Sequence[DatasetSpecification]] = (
    DatasetSpecification(
        site_name="Kelmarsh",
        zenodo_record_url="https://zenodo.org/records/8252025",
        kmz_filename="Kelmarsh_12.3MW_6xSenvion_MM92.kmz",
        scada_archive_filenames=["Kelmarsh_SCADA_2022_4457.zip"],
    ),
    DatasetSpecification(
        site_name="Penmanshiel",
        zenodo_record_url="https://zenodo.org/records/5946808",
        kmz_filename="Penmanshiel_28.7MW_14xSenvion_MM82.kmz",
        scada_archive_filenames=[
            "Penmanshiel_SCADA_2021_WT01-10_3108.zip",
            "Penmanshiel_SCADA_2021_WT11-15_3108.zip",
        ],
    ),
)


def get_zenodo_file_url(
    filename: str,
    zenodo_record_url: str,
) -> str:
    return f"{zenodo_record_url}/files/{filename}?download=1"
