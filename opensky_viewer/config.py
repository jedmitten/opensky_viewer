import os
from enum import Enum
from typing import List, Optional

import toml
from pydantic import BaseModel

from opensky_viewer.models import BoundingBox

DEFAULT_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class OutputFormat(str, Enum):
    CSV = "csv"
    JSON = "json"


class Config(BaseModel):
    bounding_box: BoundingBox
    callsigns: Optional[List[str]] = None
    transmitter_ids: Optional[List[str]] = None
    api_key: Optional[str] = None
    data_directory: Optional[str] = None
    logging_format: Optional[str] = None
    output_format: OutputFormat = OutputFormat.CSV  # Default to CSV only


def read_config(file_path: str = "./config/local.toml") -> Config:
    with open(file_path, "r") as f:
        config = toml.load(f)

    bounding_box = BoundingBox(
        min_latitude=config["LATITUDE_MIN"],
        min_longitude=config["LONGITUDE_MIN"],
        max_latitude=config["LATITUDE_MAX"],
        max_longitude=config["LONGITUDE_MAX"],
    )

    data_directory = config.get("DATA_DIRECTORY")
    if data_directory and not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # Read output_format from config, default to CSV
    output_format_str = config.get("OUTPUT_FORMAT", "csv")
    output_format = OutputFormat(output_format_str.lower())

    return Config(
        bounding_box=bounding_box,
        callsigns=config.get("CALLSIGNS"),
        transmitter_ids=config.get("TRANSMITTER_IDS"),
        api_key=config.get("API_KEY"),
        data_directory=data_directory,
        logging_format=config.get("LOGGING_FORMAT", DEFAULT_LOGGING_FORMAT),
        output_format=output_format,
    )
