#!/usr/bin/env python3
import json
import logging
import os
import random
import re
import time
from datetime import datetime, timedelta

import pandas as pd
import pytz
from opensky_api import OpenSkyApi

from opensky_viewer.config import Config, read_config


def configure_logging(config):
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format=config.logging_format)


def fetch_flights(api, config):
    logging.info("Fetching flight data within the specified bounding box.")
    # Get states within bounding box
    states = api.get_states(bbox=config.bounding_box.to_tuple())

    if states is None or not hasattr(states, "states"):
        logging.warning("No flight data received or invalid response format.")
        return []

    # Convert state vectors to a list of dictionaries
    flights = [s.__dict__ for s in states.states if s is not None]

    logging.info(f"Found {len(flights)} aircraft in the specified area.")
    return flights


def output_data(data, config, suffix: str = None, file_format="csv"):
    if not data:
        logging.warning("No data to output.")
        return

    # Ensure the data directory exists
    data_directory = config.data_directory or "./data"
    os.makedirs(data_directory, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(
        data_directory, f"flights_data{'_' + suffix if suffix else ''}_{timestamp}.{file_format.value}"
    )

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


def fetch_once(api, config):
    data = fetch_flights(api, config)
    output_data(data, config, file_format=config.output_format or "csv")
    return [data]


def fetch_n_times(api, config, n, delay, random_backoff):
    datasets = []
    for i in range(n):
        logging.info(f"Fetching data... ({i + 1}/{n})")
        data = fetch_flights(api, config)
        datasets.append(data)
        logging.debug(f"Fetched {len(data)} flights.")
        output_data(data, config, file_format=config.output_format or "csv")  # Write after each fetch
        if i < n - 1:  # Avoid sleeping after the last fetch
            logging.debug(f"Sleeping for {delay} seconds.")
            time.sleep(delay + (random.uniform(0, delay) if random_backoff else 0))
    return datasets


def parse_time_input(time_input):
    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", time_input):
        # ISO format (UTC)
        return datetime.strptime(time_input, "%Y-%m-%dT%H:%M:%SZ")
    else:
        # Relative time format
        match = re.match(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", time_input)
        if not match:
            raise ValueError("Invalid time format")
        hours, minutes, seconds = match.groups(default="0")
        delta = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        return datetime.now(tz=pytz.UTC) + delta


def fetch_until(api, config, time_input, delay, random_backoff):
    end_time = parse_time_input(time_input)
    datasets = []
    logging.info(f"Fetching data until {end_time} (UTC)...")
    while datetime.now(tz=pytz.UTC) < end_time:
        data = fetch_flights(api, config)
        datasets.append(data)
        output_data(data, config, file_format=config.output_format or "csv")  # Write after each fetch
        # Calculate next sleep duration and check if it would go past end_time
        sleep_time = delay + (random.uniform(0, delay) if random_backoff else 0)
        next_time = datetime.now(tz=pytz.UTC) + timedelta(seconds=sleep_time)
        if next_time >= end_time:
            break  # Avoid sleeping if next fetch would be after end_time
        time.sleep(sleep_time)
    return datasets


def fetch_continuously(api, config, delay, random_backoff):
    datasets = []
    logging.info("Fetching data continuously...")
    try:
        while True:
            data = fetch_flights(api, config)
            datasets.append(data)
            output_data(data, config, file_format=config.output_format or "csv")  # Write after each fetch
            time.sleep(delay + (random.uniform(0, delay) if random_backoff else 0))
    except KeyboardInterrupt:
        logging.info("Continuous fetch stopped by user.")
    return datasets


def handle_datasets(datasets):
    """Convert raw datasets into pandas DataFrames."""
    return [pd.DataFrame(data) for data in datasets]


def main(api: OpenSkyApi, config: Config):
    configure_logging(config)
    logging.info("Starting flight data fetch process.")

    # Fetch flights using the configuration
    flights = fetch_n_times(
        api=api,
        config=config,
        n=10,  # Number of fetches
        delay=(60 * 3),  # Delay between fetches in seconds
        random_backoff=False,  # Use random backoff
    )

    # Convert to pandas DataFrame for easier handling
    df = pd.DataFrame(flights)
    logging.info("Displaying flight data.")
    print(df)

    # Output data to file and downstream service
    output_data(flights, config, suffix="all", file_format=config.output_format or "csv")


if __name__ == "__main__":
    config = read_config("config/local.toml")
    api = OpenSkyApi()
    main(api, config)
