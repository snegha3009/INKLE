"""
Geocoding Service - Nominatim API Integration
Converts place names to geographic coordinates.
"""

import requests
from typing import Optional, Dict
import time


class GeocodingService:
    """Handles place name to coordinates conversion using Nominatim API"""
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "TourismBot/1.0 (Educational Project)"
        })
    
    def get_coordinates(self, place_name: str) -> Optional[Dict]:
        """
        Get latitude and longitude for a place name.
        
        Args:
            place_name: Name of the place to geocode
            
        Returns:
            Dict with 'lat', 'lon', and 'display_name' or None if not found
        """
        if not place_name or not place_name.strip():
            return None
            
        params = {
            "q": place_name.strip(),
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }
        
        try:
            # Nominatim requires rate limiting (1 request per second)
            time.sleep(1)
            
            response = self.session.get(
                self.BASE_URL, 
                params=params, 
                timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            if results:
                result = results[0]
                return {
                    "lat": float(result["lat"]),
                    "lon": float(result["lon"]),
                    "display_name": result.get("display_name", place_name)
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Geocoding error for '{place_name}': {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"Error parsing geocoding response: {e}")
            return None


# For testing
if __name__ == "__main__":
    service = GeocodingService()
    
    # Test cases
    test_places = ["Bangalore", "Paris", "InvalidCity12345"]
    
    for place in test_places:
        print(f"\nTesting: {place}")
        coords = service.get_coordinates(place)
        if coords:
            print(f"  ✓ Found: {coords['display_name']}")
            print(f"  Coordinates: ({coords['lat']}, {coords['lon']})")
        else:
            print(f"  ✗ Not found")