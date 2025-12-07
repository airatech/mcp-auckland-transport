# Auckland Transport MCP Server

A Model Context Protocol (MCP) server for connecting to the Auckland Transport API. This server provides tools to search for public transport stops and retrieve transit information using the General Transit Feed Specification (GTFS) format.

![Auckland Transport MCP Server](auckland_transport_mcp.gif)

## Features

- **Stop Search**: Search for Auckland Transport stops by name (case-insensitive substring match)
- **Stop Trip Information**: Retrieve scheduled trips and timetables for specific stops
- **GTFS Integration**: Uses General Transit Feed Specification for standardized transit data exchange
- **FastMCP Framework**: Built on FastMCP for easy MCP server development
- **Type Safety**: Full type hints and Pydantic models for data validation

## Prerequisites

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Auckland Transport API credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd auckland_transport
```

2. Install dependencies using uv:
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with your Auckland Transport API credentials:

```env
AT_BASE_URL=https://api.at.govt.nz/gtfs/v3
AT_API_KEY=your_api_key_here
```

**Note**: Make sure to add `.env` to your `.gitignore` file (already included) to keep your API keys secure.

## Usage

### Running the MCP Server

Start the MCP server:

```bash
python src/app.py
```

### Testing

Run the test script to verify the connection:

```bash
python src/test.py
```

### Using the Tools

The server provides the following MCP tools:

#### `search_stop(name: str) -> StopResponse`

Searches for Auckland Transport stops by name (case-insensitive substring match).

**Parameters:**
- `name` (str): The stop name to search for

**Returns:**
- `StopResponse`: A Pydantic model containing a list of matching stops with attributes including:
  - `stop_id`: Unique identifier for the stop
  - `stop_code`: Public-facing stop code
  - `stop_name`: Name of the stop
  - `stop_lat`: Latitude coordinate
  - `stop_lon`: Longitude coordinate
  - `location_type`: Type of location (0=stop, 1=station, etc.)
  - `wheelchair_boarding`: Wheelchair accessibility information (0=unknown, 1=accessible, 2=not accessible)

**Example:**
```python
from at_service import ATService

at_service = ATService()
result = at_service.search_stop("University")
print(result.model_dump_json())
```

#### `get_stop_trips_by_stop_id(stop_id: str) -> StopTripResponse`

Retrieves scheduled trips for a specific stop on the current date and hour.

**Parameters:**
- `stop_id` (str): The unique identifier of the stop

**Returns:**
- `StopTripResponse`: A Pydantic model containing a list of stop trips with attributes including:
  - `arrival_time`: Scheduled arrival time (HH:MM:SS format)
  - `departure_time`: Scheduled departure time (HH:MM:SS format)
  - `route_id`: Identifier for the route
  - `trip_headsign`: Text displayed on the vehicle for this trip
  - `stop_headsign`: Text displayed on signage at the stop
  - `stop_sequence`: Order of this stop in the trip sequence
  - `direction_id`: Direction of travel (0 or 1)
  - `service_date`: Date of service (YYYY-MM-DD format)
  - `shape_id`: Identifier for the shape/geometry of the route
  - `pickup_type`: Pickup type (0=regular, 1=none, 2=phone, 3=driver)
  - `drop_off_type`: Drop-off type (0=regular, 1=none, 2=phone, 3=driver)

**Example:**
```python
from at_service import ATService

at_service = ATService()
# First, search for a stop to get its stop_id
stops = at_service.search_stop("University")
if stops.data:
    stop_id = stops.data[0].attributes.stop_id
    trips = at_service.get_stop_trips_by_stop_id(stop_id)
    print(trips.model_dump_json())
```

## Project Structure

```
auckland-transport/
├── src/
│   ├── app.py          # FastMCP server application with MCP tools
│   ├── at_service.py   # Auckland Transport API service class
│   ├── gtfs_types.py   # Pydantic models for GTFS data structures
│   ├── test.py         # Test script for API connectivity
│   └── utils.py        # Utility functions
├── .env                # Environment variables (not in repo, create locally)
├── pyproject.toml      # Project dependencies and metadata
├── uv.lock             # Dependency lock file
└── README.md           # This file
```

## Dependencies

- `fastmcp>=2.13.2`: FastMCP framework for building MCP servers
- `dotenv>=0.9.9`: Environment variable management
- `pydantic`: Data validation and modeling for GTFS structures
- `requests`: HTTP library for API calls

**Note**: The project uses `uv` for dependency management. All dependencies are specified in `pyproject.toml`.

## Development

### Adding New Tools

To add new MCP tools, edit `src/app.py` and add new tool functions decorated with `@mcp.tool`:

```python
@mcp.tool
def your_new_tool(param: str) -> ReturnType:
    # Your implementation
    return result
```

### API Reference

The Auckland Transport API uses GTFS (General Transit Feed Specification) for data exchange. For more information about the API, visit the [Auckland Transport API documentation](https://api.at.govt.nz/).

#### Data Models

The project uses Pydantic models defined in `gtfs_types.py` to validate and structure API responses:

- **StopAttributes**: Contains stop location and accessibility information
- **Stop**: Represents a single stop resource with type, ID, and attributes
- **StopResponse**: Container for multiple stop search results
- **StopTripAttributes**: Contains trip timing, route, and service information
- **StopTrip**: Represents a single stop trip resource
- **StopTripResponse**: Container for multiple stop trip results

All models follow the GTFS standard and are fully typed for better IDE support and error checking.

## Troubleshooting

### Common Issues

1. **API Key Not Found**: Ensure your `.env` file exists in the root directory and contains both `AT_BASE_URL` and `AT_API_KEY`.

2. **Empty Results**: The API returns data for the current date and hour. If searching for trips, ensure there are scheduled services at the current time.

3. **Connection Errors**: Verify your internet connection and that the Auckland Transport API is accessible from your network.

## References

- [GTFS Static Overview - Google Developers](https://developers.google.com/transit/gtfs) - Official Google documentation for GTFS (General Transit Feed Specification)
- [GTFS Documentation - gtfs.org](https://gtfs.org/documentation/overview/) - Official GTFS specification documentation maintained by MobilityData

## License

MIT License

Copyright (c) 2025 Aira Technologies Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

