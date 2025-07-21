from enum import IntEnum

from pydantic import BaseModel


class BoundingBox(BaseModel):
    min_latitude: float  # Minimum latitude
    min_longitude: float  # Minimum longitude
    max_latitude: float  # Maximum latitude
    max_longitude: float  # Maximum longitude

    def to_tuple(self):
        return (
            self.min_latitude,
            self.max_latitude,
            self.min_longitude,
            self.max_longitude,
        )


class AircraftCategory(IntEnum):
    NO_INFO = 0
    NO_ADSB_INFO = 1
    LIGHT = 2
    SMALL = 3
    LARGE = 4
    HIGH_VORTEX_LARGE = 5
    HEAVY = 6
    HIGH_PERFORMANCE = 7
    ROTORCRAFT = 8
    GLIDER = 9
    LIGHTER_THAN_AIR = 10
    PARACHUTIST = 11
    ULTRALIGHT = 12
    RESERVED = 13
    UAV = 14
    SPACE = 15
    SURFACE_EMERGENCY = 16
    SURFACE_SERVICE = 17
    POINT_OBSTACLE = 18
    CLUSTER_OBSTACLE = 19
    LINE_OBSTACLE = 20

    @classmethod
    def description(cls, value):
        descriptions = {
            0: "No information at all",
            1: "No ADS-B Emitter Category Information",
            2: "Light (< 15500 lbs)",
            3: "Small (15500 to 75000 lbs)",
            4: "Large (75000 to 300000 lbs)",
            5: "High Vortex Large (aircraft such as B-757)",
            6: "Heavy (> 300000 lbs)",
            7: "High Performance (> 5g acceleration and 400 kts)",
            8: "Rotorcraft",
            9: "Glider / sailplane",
            10: "Lighter-than-air",
            11: "Parachutist / Skydiver",
            12: "Ultralight / hang-glider / paraglider",
            13: "Reserved",
            14: "Unmanned Aerial Vehicle",
            15: "Space / Trans-atmospheric vehicle",
            16: "Surface Vehicle – Emergency Vehicle",
            17: "Surface Vehicle – Service Vehicle",
            18: "Point Obstacle (includes tethered balloons)",
            19: "Cluster Obstacle",
            20: "Line Obstacle",
        }
        return descriptions.get(value, "Unknown")

    @classmethod
    def to_dataframe(cls):
        """Convert the enum to a DataFrame for easier display."""
        import pandas as pd

        df = pd.DataFrame(
            [(cat.name, cat.value, cls.description(cat.value)) for cat in cls], columns=["Name", "Value", "Description"]
        )
        df = df.set_index("Value")
        return df
