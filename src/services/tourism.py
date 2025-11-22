"""
Tourism Service - Overpass API Integration
Fetches tourist attractions from OpenStreetMap data.
"""

import requests
from typing import List, Dict, Optional


class TourismService:
    """Handles tourist attractions retrieval using Overpass API"""
    
    BASE_URL = "https://overpass-api.de/api/interpreter"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_attractions(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int = 5000,
        max_results: int = 5
    ) -> List[str]:
        """
        Get tourist attractions near given coordinates.
        
        Args:
            latitude: Geographic latitude
            longitude: Geographic longitude
            radius: Search radius in meters (default: 5000m = 5km)
            max_results: Maximum number of results to return
            
        Returns:
            List of attraction names
        """
        # Overpass QL query to find tourism attractions
        query = f"""
        [out:json][timeout:25];
        (
          node["tourism"](around:{radius},{latitude},{longitude});
          way["tourism"](around:{radius},{latitude},{longitude});
          relation["tourism"](around:{radius},{latitude},{longitude});
        );
        out center tags {max_results * 3};
        """
        
        try:
            response = self.session.post(
                self.BASE_URL,
                data={"data": query},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            attractions = []
            seen_names = set()
            
            for element in data.get("elements", []):
                tags = element.get("tags", {})
                name = tags.get("name")
                
                # Only include named attractions, avoid duplicates
                if name and name not in seen_names:
                    attractions.append(name)
                    seen_names.add(name)
                    
                    if len(attractions) >= max_results:
                        break
            
            return attractions
            
        except requests.exceptions.RequestException as e:
            print(f"Tourism API error: {e}")
            return []
        except (KeyError, ValueError) as e:
            print(f"Error parsing tourism response: {e}")
            return []
    
    def format_attractions_list(self, attractions: List[str], place_name: str) -> str:
        """Format attractions list into human-readable description"""
        if not attractions:
            return f"No tourist attractions found in {place_name}"
        
        attractions_str = ", ".join(attractions)
        return f"List of {len(attractions)} places: {attractions_str}"


# For testing
if __name__ == "__main__":
    service = TourismService()
    
    # Test with Bangalore coordinates
    print("Testing Tourism API...")
    print("Location: Bangalore (12.9716, 77.5946)\n")
    
    attractions = service.get_attractions(12.9716, 77.5946)
    if attractions:
        print(f"✓ Found {len(attractions)} attractions:")
        for i, attraction in enumerate(attractions, 1):
            print(f"  {i}. {attraction}")
        print(f"\nFormatted: {service.format_attractions_list(attractions, 'Bangalore')}")
    else:
        print("✗ No attractions found") 