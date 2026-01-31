"""
Geo Utilities
Geographic and location-related utilities.
"""

from typing import Optional, Tuple, Dict, Any
import math


# Country codes and names
SUPPORTED_COUNTRIES = {
    "PK": "Pakistan",
    "GB": "United Kingdom",
    "US": "United States",
    "CA": "Canada",
    "AU": "Australia",
    "DE": "Germany",
    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia",
    "MY": "Malaysia",
}

# Major cities with coordinates (for distance calculations)
MAJOR_CITIES = {
    "Islamabad": (33.6844, 73.0479),
    "Karachi": (24.8607, 67.0011),
    "Lahore": (31.5497, 74.3436),
    "London": (51.5074, -0.1278),
    "Manchester": (53.4839, -2.2446),
    "New York": (40.7128, -74.0060),
    "Toronto": (43.6532, -79.3832),
    "Sydney": (-33.8688, 151.2093),
    "Melbourne": (-37.8136, 144.9631),
    "Berlin": (52.5200, 13.4050),
    "Dubai": (25.2048, 55.2708),
}


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate distance between two points on Earth using Haversine formula.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
    
    Returns:
        float: Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (
        math.sin(delta_lat / 2) ** 2 +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def get_country_name(country_code: str) -> Optional[str]:
    """Get country name from ISO code."""
    return SUPPORTED_COUNTRIES.get(country_code.upper())


def get_city_coordinates(city_name: str) -> Optional[Tuple[float, float]]:
    """Get coordinates for a known city."""
    return MAJOR_CITIES.get(city_name)


def calculate_city_distance(city1: str, city2: str) -> Optional[float]:
    """
    Calculate distance between two cities.
    
    Returns:
        Optional[float]: Distance in kilometers, or None if city not found
    """
    coords1 = get_city_coordinates(city1)
    coords2 = get_city_coordinates(city2)
    
    if not coords1 or not coords2:
        return None
    
    return haversine_distance(coords1[0], coords1[1], coords2[0], coords2[1])


def get_timezone_for_country(country_code: str) -> str:
    """Get primary timezone for a country."""
    timezones = {
        "PK": "Asia/Karachi",
        "GB": "Europe/London",
        "US": "America/New_York",
        "CA": "America/Toronto",
        "AU": "Australia/Sydney",
        "DE": "Europe/Berlin",
        "AE": "Asia/Dubai",
        "SA": "Asia/Riyadh",
        "MY": "Asia/Kuala_Lumpur",
    }
    return timezones.get(country_code.upper(), "UTC")


def format_address(
    street: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    country: Optional[str] = None,
) -> str:
    """Format address components into a single string."""
    parts = [p for p in [street, city, state, postal_code, country] if p]
    return ", ".join(parts)


def parse_coordinates(coord_string: str) -> Optional[Tuple[float, float]]:
    """
    Parse coordinate string into lat/lon tuple.
    
    Accepts formats:
    - "33.6844, 73.0479"
    - "33.6844,73.0479"
    - "33.6844 73.0479"
    """
    try:
        # Try comma separator
        if "," in coord_string:
            parts = coord_string.split(",")
        else:
            parts = coord_string.split()
        
        if len(parts) != 2:
            return None
        
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        
        # Validate ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return (lat, lon)
        
        return None
    except ValueError:
        return None


def get_cost_of_living_index(city: str) -> Optional[Dict[str, Any]]:
    """
    Get cost of living information for a city.
    Used for the "Reality Tools" feature.
    """
    # Sample data - in production, use a real API
    cost_data = {
        "London": {
            "index": 85.0,
            "rent_1br_center": 1800,
            "rent_1br_outside": 1200,
            "groceries_monthly": 300,
            "transport_monthly": 150,
            "currency": "GBP",
        },
        "Sydney": {
            "index": 80.0,
            "rent_1br_center": 2000,
            "rent_1br_outside": 1400,
            "groceries_monthly": 400,
            "transport_monthly": 120,
            "currency": "AUD",
        },
        "Islamabad": {
            "index": 25.0,
            "rent_1br_center": 30000,
            "rent_1br_outside": 20000,
            "groceries_monthly": 25000,
            "transport_monthly": 5000,
            "currency": "PKR",
        },
    }
    
    return cost_data.get(city)
