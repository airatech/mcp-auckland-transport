"""Pydantic models for General Transit Feed Specification (GTFS) data structures.

This module defines the data models used to parse and validate responses from
the Auckland Transport API, which follows the GTFS standard for transit data.
"""

from pydantic import BaseModel
from typing import List


class StopAttributes(BaseModel):
    """Attributes of a transit stop in GTFS format.
    
    Attributes:
        location_type: Type of location (0=stop, 1=station, etc.)
        stop_code: Public-facing stop code
        stop_id: Unique identifier for the stop
        stop_lat: Latitude coordinate of the stop
        stop_lon: Longitude coordinate of the stop
        stop_name: Name of the stop
        wheelchair_boarding: Wheelchair accessibility (0=unknown, 1=accessible, 2=not accessible)
    """
    location_type: int
    stop_code: str
    stop_id: str
    stop_lat: float
    stop_lon: float
    stop_name: str
    wheelchair_boarding: int

class Stop(BaseModel):
    """GTFS stop resource with type, ID, and attributes.
    
    Attributes:
        type: Resource type (typically "stop")
        id: Unique identifier for the stop resource
        attributes: Stop attributes containing stop details
    """
    type: str
    id: str
    attributes: StopAttributes


class StopResponse(BaseModel):
    """Response model containing a list of stops.
    
    Attributes:
        data: List of Stop objects matching the search criteria
    """
    data: List[Stop]


class StopTripAttributes(BaseModel):
    """Attributes of a stop trip in GTFS format.
    
    Represents a scheduled trip at a specific stop, including timing,
    route information, and service details.
    
    Attributes:
        arrival_time: Scheduled arrival time (HH:MM:SS format)
        departure_time: Scheduled departure time (HH:MM:SS format)
        direction_id: Direction of travel (0 or 1)
        drop_off_type: Drop-off type (0=regular, 1=none, 2=phone, 3=driver)
        pickup_type: Pickup type (0=regular, 1=none, 2=phone, 3=driver)
        route_id: Identifier for the route
        service_date: Date of service (YYYY-MM-DD format)
        shape_id: Identifier for the shape/geometry of the route
        stop_headsign: Text displayed on signage at the stop
        stop_id: Unique identifier for the stop
        stop_sequence: Order of this stop in the trip sequence
        trip_headsign: Text displayed on the vehicle for this trip
    """
    arrival_time: str
    departure_time: str
    direction_id: int
    drop_off_type: int
    pickup_type: int
    route_id: str
    service_date: str
    shape_id: str
    stop_headsign: str
    stop_id: str
    stop_sequence: int
    trip_headsign: str


class StopTrip(BaseModel):
    """GTFS stop trip resource with type, ID, and attributes.
    
    Attributes:
        type: Resource type (typically "stoptrip")
        id: Unique identifier for the stop trip resource
        attributes: Stop trip attributes containing trip details
    """
    type: str
    id: str
    attributes: StopTripAttributes


class StopTripResponse(BaseModel):
    """Response model containing a list of stop trips.
    
    Attributes:
        data: List of StopTrip objects for the specified stop
    """
    data: List[StopTrip]