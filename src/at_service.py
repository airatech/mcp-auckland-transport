"""Auckland Transport API Service.

This module provides a service class for interacting with the Auckland Transport
API. It handles authentication, request formatting, and response parsing for
GTFS-based transit data.
"""

import os
import requests
from datetime import datetime

from gtfs_types import StopResponse
from gtfs_types import StopTripResponse


class ATService:
    """Service class for interacting with the Auckland Transport API.
    
    This class provides methods to search for stops and retrieve stop trip
    information from the Auckland Transport API. It handles API authentication,
    URL construction, and response parsing.
    
    Attributes:
        base_url (str): Base URL for the Auckland Transport API
        api_key (str): API key for authentication
        headers (dict): HTTP headers including authentication
    """

    URL_MAP = {
        "search_stop": "/stops?filter[date]={journey_date}",
        'stop_trips_by_stop_id': "/stops/{stop_id}/stoptrips?filter[date]={journey_date}&filter[start_hour]={journey_hour}"
    }

    def __init__(self):
        """Initialize the ATService with API credentials from environment variables.
        
        Reads AT_BASE_URL and AT_API_KEY from environment variables and sets up
        HTTP headers for API requests.
        """
        self.base_url = os.getenv("AT_BASE_URL")  
        self.api_key = os.getenv("AT_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": os.getenv("AT_API_KEY")
        }

    def _make_request(self, url: str, method: str = "GET", params: dict = None, data: dict = None) -> dict:
        """Make an HTTP request to the Auckland Transport API.
        
        Args:
            url: The full URL to make the request to
            method: HTTP method (default: "GET")
            params: Optional query parameters
            data: Optional request body data
            
        Returns:
            dict: JSON response from the API
        """
        response = requests.request(method, url, headers=self.headers, params=params, data=data)
        return response.json()

    def _get_url(self, url: str, **kwargs) -> str:
        """Construct a full API URL from a URL template key and parameters.
        
        Args:
            url: Key from URL_MAP dictionary
            **kwargs: Parameters to format into the URL template
            
        Returns:
            str: Complete API URL with base URL and formatted path
        """
        return f"{self.base_url}{self.URL_MAP[url].format(**kwargs)}"  

    def _get_date_time(self) -> str:
        """Get the current date in YYYY-MM-DD format.
        
        Returns:
            str: Current date formatted as YYYY-MM-DD
        """
        return datetime.now().strftime("%Y-%m-%d")

    def _get_hour(self) -> str:
        """Get the current hour in HH format (24-hour).
        
        Returns:
            str: Current hour formatted as HH (00-23)
        """
        return datetime.now().strftime("%H")

    def search_stop(self, name: str) -> StopResponse:
        """Search for Auckland Transport stops by name.
        
        Performs a case-insensitive substring search on stop names. Returns
        all stops that contain the search term in their name.
        
        Args:
            name: The stop name to search for (case-insensitive substring match)
            
        Returns:
            StopResponse: Response containing a list of matching stops. Returns
            empty list if name is None or empty string.
        """
        if name is None or name == "":
            return StopResponse(data=[])
        name = name.strip()
        url = self._get_url("search_stop", journey_date=self._get_date_time())
        stops = self._make_request(url, "GET")
        stop_response = StopResponse.model_validate(stops)
        
        found_stops = StopResponse(data=[])
        for stop in stop_response.data:
            # Search for substring of stop name
            if name.lower() in stop.attributes.stop_name.lower():
                found_stops.data.append(stop)

        return found_stops
    
    def get_stop_trips_by_stop_id(self, stop_id: str) -> StopTripResponse:
        """Get stop trips for a specific stop ID.
        
        Retrieves all trips scheduled for a given stop on the current date
        and hour. Returns trip information including arrival/departure times,
        route information, and trip details.
        
        Args:
            stop_id: The unique identifier of the stop
            
        Returns:
            StopTripResponse: Response containing a list of stop trips with
            attributes including arrival_time, departure_time, route_id,
            trip_headsign, and other GTFS trip information. Returns empty list
            if stop_id is None or empty string.
        """
        if stop_id is None or stop_id == "":
            return StopTripResponse(data=[])
        stop_id = stop_id.strip()
        url = self._get_url("stop_trips_by_stop_id", stop_id=stop_id, 
                            journey_date=self._get_date_time(), 
                            journey_hour=self._get_hour())
        stop_trips = self._make_request(url, "GET")
        stop_trip_response = StopTripResponse.model_validate(stop_trips)
        return stop_trip_response
