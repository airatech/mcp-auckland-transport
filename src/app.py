"""MCP Server for connecting to the Auckland Transport API.

This module provides a Model Context Protocol (MCP) server that connects to the
Auckland Transport API. The API uses General Transit Feed Specification (GTFS)
for data exchange, providing standardized transit information.

The server exposes tools for:
- Searching for public transport stops by name
- Retrieving stop trips and schedules by stop ID
"""

from fastmcp import FastMCP
from dotenv import load_dotenv
from at_service import ATService
from gtfs_types import StopResponse
from gtfs_types import StopTripResponse

load_dotenv()

at_service = ATService()

mcp = FastMCP(name="auckland-transport")


@mcp.tool
def search_stop(name: str) -> StopResponse:
    """Search for Auckland Transport stops by name (case-insensitive substring match).
    
    Args:
        name: The stop name to search for
        
    Returns:
        StopResponse: A response containing a list of matching stops with attributes including
        stop_id, stop_code, stop_name, stop_lat, stop_lon, location_type, and wheelchair_boarding
    """
    return at_service.search_stop(name)


@mcp.tool
def get_stop_trips_by_stop_id(stop_id: str) -> StopTripResponse:
    """Get the stop trips by stop id.
    Args:
        stop_id: The stop id to get the trips for
        
    Returns:
        StopTripResponse: A response containing a list of matching stop trips with attributes including
        arrival_time, departure_time, direction_id, drop_off_type, pickup_type, route_id, service_date, 
        shape_id, stop_headsign, stop_id, stop_sequence, and trip_headsign
    """
    return at_service.get_stop_trips_by_stop_id(stop_id)


if __name__ == "__main__":
    """Run the MCP server when executed directly."""
    mcp.run()
