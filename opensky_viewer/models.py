from pydantic import BaseModel
from typing import Optional

class BoundingBox(BaseModel):
    min_latitude: float  # Minimum latitude
    min_longitude: float  # Minimum longitude
    max_latitude: float  # Maximum latitude
    max_longitude: float  # Maximum longitude

    def to_tuple(self):
        return (self.min_latitude, self.max_latitude, self.min_longitude, self.max_longitude)
