#!/usr/bin/env python3

from opensky_api import OpenSkyApi
from datetime import datetime
import pandas as pd
from opensky_viewer.config import read_config
import logging
import os
import json
import requests

# Configure logging
def configure_logging(config):
    # Configure logging
    logging.basicConfig(level=logging.INFO, format=config.logging_format)

def fetch_flights(api, config):
    logging.info("Fetching flight data within the specified bounding box.")
    # Get states within bounding box
    states = api.get_states(
        bbox=config.bounding_box.to_tuple()
    )

    if states is None or not hasattr(states, 'states'):
        logging.warning("No flight data received or invalid response format.")
        return []

    # Convert state vectors to a list of dictionaries
    flights = [
        s.__dict__ for s in states.states if s is not None
    ]

    logging.info(f"Found {len(flights)} aircraft in the specified area.")
    return flights

def output_data(data, config, file_format="csv", send_downstream=False):
    if not data:
        logging.warning("No data to output.")
        return

    # Ensure the data directory exists
    data_directory = config.data_directory or "./data"
    os.makedirs(data_directory, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(data_directory, f"flights_data_{timestamp}.{file_format}")

    # Save data to file
    if file_format == "csv":
        pd.DataFrame(data).to_csv(file_path, index=False)
        logging.info(f"Flight data saved to {file_path} as CSV.")
    elif file_format == "json":
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Flight data saved to {file_path} as JSON.")
    else:
        logging.error(f"Unsupported file format: {file_format}")

    # Send data to downstream service if enabled
    if send_downstream:
        downstream_url = config.downstream_url
        if not downstream_url:
            logging.error("Downstream URL is not configured.")
            return

        try:
            response = requests.post(downstream_url, json=data)
            if response.status_code == 200:
                logging.info("Data successfully sent to downstream service.")
            else:
                logging.error(f"Failed to send data downstream. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            logging.error(f"Error sending data downstream: {e}")

def main():
    # Read configuration from config file
    config_path = "config/local.toml"
    config = read_config(config_path)

    # Configure logging with the config
    configure_logging(config)

    logging.info("Creating OpenSky API instance.")
    # Create OpenSky API instance
    api = OpenSkyApi()

    logging.info("Starting flight data fetch process.")
    # Fetch flights using the configuration
    flights = fetch_flights(api, config)

    # Convert to pandas DataFrame for easier handling
    df = pd.DataFrame(flights)
    logging.info("Displaying flight data.")
    print(df)

    # Output data to file and downstream service
    output_data(flights, config, file_format="csv", send_downstream=True)
    output_data(flights, config, file_format="json", send_downstream=False)


if __name__ == "__main__":
    main()
