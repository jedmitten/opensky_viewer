## API Return Data Headers

The OpenSky API returns the following fields for each aircraft state. These are used as CSV headers in the output:

| Header           | Description                                                                                   |
|------------------|----------------------------------------------------------------------------------------------|
| `icao24`         | Unique ICAO 24-bit address of the transponder                                                |
| `callsign`       | Callsign of the vehicle (8 chars, can be null or empty)                                      |
| `origin_country` | Country name inferred from the ICAO 24-bit address                                           |
| `time_position`  | Unix timestamp for the last position update (can be null)                                    |
| `last_contact`   | Unix timestamp for the last update received from the transponder                             |
| `longitude`      | WGS-84 longitude in decimal degrees (can be null)                                            |
| `latitude`       | WGS-84 latitude in decimal degrees (can be null)                                             |
| `baro_altitude`  | Barometric altitude in meters (can be null)                                                  |
| `on_ground`      | Boolean indicating if the aircraft is on the ground                                          |
| `velocity`       | Velocity over ground in m/s (can be null)                                                    |
| `true_track`     | True track in decimal degrees clockwise from north (can be null)                             |
| `vertical_rate`  | Vertical rate in m/s. Positive means climbing, negative means descending (can be null)       |
| `sensors`        | List of sensor IDs that received the message (can be null)                                   |
| `geo_altitude`   | Geometric altitude in meters (can be null)                                                   |
| `squawk`         | Transponder code (Squawk) (can be null)                                                      |
| `spi`            | Boolean indicating if flight status is special purpose indicator                             |
| `position_source`| Source of position information: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT                            |
| `category`       | Aircraft category (integer, can be null)                                                     |

These fields are included in each row of the output CSV or

## Fetch Functions

The project provides several fetch functions to retrieve flight data from the OpenSky API, each tailored for different use cases:

| Function             | Intent                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `fetch_once`         | Fetches flight data a single time and returns the result.                                   |
| `fetch_n_times`      | Fetches flight data a specified number of times, with a configurable delay between fetches. |
| `fetch_until`        | Fetches flight data repeatedly until a specified time is reached (relative or absolute).    |
| `fetch_continuously` | Continuously fetches flight data at a set interval until manually stopped.                  |

- **`fetch_once`**: Use when you want a snapshot of current flight data.
- **`fetch_n_times`**: Use for periodic sampling, e.g., every minute for 10 minutes.
- **`fetch_until`**: Use to collect data up to a future time (e.g., "5 minutes from now" or a specific UTC timestamp).
- **`fetch_continuously`**: Use for ongoing monitoring; stops only when the process is interrupted.

Each function returns a list of datasets, which can then be converted to DataFrames and saved or

## Configuration

All runtime options are set in the `config/local.toml` file.  
You can copy and edit `config/example.toml` as a starting point:

```sh
cp config/example.toml config/local.toml
```

**Key configuration fields:**

- `LATITUDE_MIN`, `LONGITUDE_MIN`, `LATITUDE_MAX`, `LONGITUDE_MAX`:  
  Define the bounding box for the area of interest.
- `DATA_DIRECTORY`:  
  Directory where output files will be saved (default: `./data`).
- `OUTPUT_FORMAT`:  
  Output file format, either `"csv"` or `"json"` (default: `"csv"`).
- `LOGGING_FORMAT`:  
  (Optional) Format for log messages.
- `CALLSIGNS`:  
  (Optional) List of callsigns to filter (uncomment and edit as needed).
- `TRANSMITTER_IDS`:  
  (Optional) List of transmitter IDs to filter (uncomment and edit as needed).
- `API_KEY`:  
  (Optional) API key for OpenSky (leave blank or remove if not needed).

**Example:**
```toml
LATITUDE_MIN = 32.0
LONGITUDE_MIN = -118.0
LATITUDE_MAX = 33.0
LONGITUDE_MAX = -117.0
DATA_DIRECTORY = "./data"
OUTPUT_FORMAT = "csv"
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# API_KEY = ""
```

**Note:**  
- If a field is not set, the application will use a sensible default (e.g., CSV for output format).
- Make sure the `DATA_DIRECTORY` exists or let the application create it on first run.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1. **Install Poetry** (if you don't have it):
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. **Clone this repository** (if you haven't already):
    ```sh
    git clone <relative/path/to/opensky_viewer>
    cd opensky_viewer
    ```

3. **Install dependencies**:
    ```sh
    poetry install
    ```

4. **(Optional) Add this repo as a dependency from another local project**:
    ```sh
    poetry add ../opensky_viewer
    ```

5. **Activate the Poetry shell**:
    ```sh
    poetry shell
    ```

6. **Run the main script**:
    ```sh
    python -m opensky_viewer.main
    ```

Make sure to configure your settings in `config/local.toml`

## Data Directory Usage

All fetched flight data is saved in the `data` directory (by default `opensky_viewer/data/`).  
Each fetch operation writes a new file with a timestamp in its name, in either CSV or JSON format depending on your configuration.

- **Location:**  
  The directory can be configured in your `config/local.toml` file with the `data_directory` option.
- **File Naming:**  
  Files are named like `flights_data_<timestamp>.csv` or `flights_data_<timestamp>.json`.
- **Purpose:**  
  This directory serves as a persistent store for all raw flight data you collect, making it easy to analyze or compare datasets later.

**Example:**
```
opensky_viewer/
  data/
    flights_data_20250622_210254.csv
    flights_data_20250622_210554.csv
    ...
```

Make sure the directory exists or is correctly set in your config before running fetch commands.

## Output: Main vs. Individual Fetch Results

- **Individual Fetch Output:**  
  After each fetch operation (whether using `fetch_once`, `fetch_n_times`, `fetch_until`, or `fetch_continuously`), the results are immediately written to a file in the `data` directory. Each file is timestamped and contains only the results from that specific fetch. This ensures you have a record of every individual data collection event.

- **Main Output (Summary/Analysis):**  
  After all fetches are complete, the main script can aggregate or analyze the collected datasets. For example, it may combine all fetched data into a single pandas DataFrame for further processing, display, or comparison. This summary or analysis is typically shown in the console or used for downstream analysis, but is not automatically written to a file unless you add that logic.

**In summary:**  
- Every fetch writes its own file in the `data` directory.
- The main output is an in-memory aggregation or analysis of all fetches, useful for further downstream inputs

