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