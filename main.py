#!/usr/bin/env python3

from opensky_api import OpenSkyApi
from datetime import datetime
import pandas as pd
from opensky_viewer.config import read_config

def fetch_flights(api, config):
    # Get states within bounding box
    states = api.get_states(
        bbox=config.bounding_box.to_tuple()
    )

    if states is None:
        print("No flight data received")
        return

    # Create a list to store flight data
    flights = []
    for s in states.states:
        flight = {
            'icao24': s.icao24,
            'callsign': s.callsign,
            'origin_country': s.origin_country,
            'longitude': s.longitude,
            'latitude': s.latitude,
            'altitude': s.baro_altitude,
            'on_ground': s.on_ground,
            'velocity': s.velocity,
            'heading': s.heading,
            'vertical_rate': s.vertical_rate,
            'timestamp': datetime.fromtimestamp(s.time_position) if s.time_position else None
        }
        flights.append(flight)

    # Convert to pandas DataFrame for easier handling
    df = pd.DataFrame(flights)

    # Display results
    print(f"\nFound {len(flights)} aircraft in the specified area:")
    print(df)

    # Save to CSV
    df.to_csv("flights_data.csv", index=False)
    print("\nFlight data saved to flights_data.csv")


def main():
    # Read configuration from config file
    config_path = "config/local.toml"
    config = read_config(config_path)

    # Create OpenSky API instance
    api = OpenSkyApi()

    # Fetch flights using the configuration
    fetch_flights(api, config)


if __name__ == "__main__":
    main()
