from pydantic import BaseModel
from typing import Optional

class BoundingBox(BaseModel):
    min_latitude: float  # Minimum latitude
    min_longitude: float  # Minimum longitude
    max_latitude: float  # Maximum latitude
    max_longitude: float  # Maximum longitude

    def to_tuple(self):
        return (self.min_latitude, self.min_longitude, self.max_latitude, self.max_longitude)

class FlightData(BaseModel):
    icao24: str
    callsign: Optional[str]
    origin_country: str
    longitude: Optional[float]
    latitude: Optional[float]
    altitude: Optional[float]
    on_ground: bool
    velocity: Optional[float]
    heading: Optional[float]
    vertical_rate: Optional[float]
    timestamp: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "icao24": "a3cf6d",
                "callsign": "UAL2674",
                "origin_country": "United States",
                "longitude": -116.8293,
                "latitude": 32.7041,
                "altitude": 1790.7,
                "on_ground": False,
                "velocity": 128.91,
                "heading": 249.68,
                "vertical_rate": 1.3,
                "timestamp": "2025-06-14T12:34:56Z"
            }
        }
