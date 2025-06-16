import os
import toml
from opensky_viewer.models import BoundingBox
from pydantic import BaseModel
from typing import List, Optional

DEFAULT_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class Config(BaseModel):
    bounding_box: BoundingBox
    callsigns: Optional[List[str]] = None
    transmitter_ids: Optional[List[str]] = None
    api_key: Optional[str] = None
    data_directory: Optional[str] = None
    logging_format: Optional[str] = None

def read_config(file_path):
    with open(file_path, 'r') as f:
        config = toml.load(f)

    bounding_box = BoundingBox(
        min_latitude=config['LATITUDE_MIN'],
        min_longitude=config['LONGITUDE_MIN'],
        max_latitude=config['LATITUDE_MAX'],
        max_longitude=config['LONGITUDE_MAX']
    )

    data_directory = config.get('DATA_DIRECTORY')
    if data_directory and not os.path.exists(data_directory):
        os.makedirs(data_directory)

    return Config(
        bounding_box=bounding_box,
        callsigns=config.get('CALLSIGNS'),
        transmitter_ids=config.get('TRANSMITTER_IDS'),
        api_key=config.get('API_KEY'),
        data_directory=data_directory,
        logging_format=config.get('LOGGING_FORMAT', DEFAULT_LOGGING_FORMAT)
    )
