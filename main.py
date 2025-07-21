#!/usr/bin/env python3
import pandas as pd
from opensky_api import OpenSkyApi

from opensky_viewer.api import fetch_n_times, write_data
from opensky_viewer.config import Config, read_config
from opensky_viewer.logging import configure_logger

logger = configure_logger("main")


def main(api: OpenSkyApi, config: Config):
    logger.info("Starting flight data fetch process.")

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
    logger.info("Displaying flight data.")
    print(df)

    # Output data to file and downstream service
    write_data(flights, config, suffix="all", file_format=config.output_format or "csv")


if __name__ == "__main__":
    config = read_config("config/local.toml")
    api = OpenSkyApi()
    main(api, config)
