"""
LangChain Tool Definitions
Wraps API services as LangChain tools for agent use.
"""

from langchain.tools import Tool
from typing import Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from services.tourism import TourismService
from services.weather import WeatherService
from services.geocoding import GeocodingService



class TourismTools:
    """Factory class for creating LangChain tools"""
    
    def __init__(self):
        self.geocoding = GeocodingService()
        self.weather = WeatherService()
        self.tourism = TourismService()
    
    def _weather_agent_function(self, place_name: str) -> str:
        """
        Weather Agent - Gets current weather for a location.
        
        Args:
            place_name: Name of the place (e.g., "Bangalore", "Paris")
            
        Returns:
            Weather description string
        """
        # Get coordinates
        coords = self.geocoding.get_coordinates(place_name)
        if not coords:
            return f"I don't know this place exists: {place_name}"
        
        # Get weather
        weather_data = self.weather.get_weather(coords["lat"], coords["lon"])
        if not weather_data:
            return f"Could not retrieve weather data for {place_name}"
        
        # Format response
        location = coords["display_name"].split(",")[0]  # Get main place name
        description = self.weather.format_weather_description(weather_data)
        
        return f"In {location} {description}."
    
    def _places_agent_function(self, place_name: str) -> str:
        """
        Places Agent - Gets tourist attractions for a location.
        
        Args:
            place_name: Name of the place (e.g., "Bangalore", "Paris")
            
        Returns:
            List of tourist attractions
        """
        # Get coordinates
        coords = self.geocoding.get_coordinates(place_name)
        if not coords:
            return f"I don't know this place exists: {place_name}"
        
        # Get attractions
        attractions = self.tourism.get_attractions(coords["lat"], coords["lon"])
        if not attractions:
            return f"No tourist attractions found in {place_name}"
        
        # Format response
        location = coords["display_name"].split(",")[0]
        formatted = self.tourism.format_attractions_list(attractions, location)
        
        return formatted
    
    def create_tools(self):
        """Create and return LangChain tools for the agents"""
        
        weather_tool = Tool(
            name="WeatherAgent",
            func=self._weather_agent_function,
            description=(
                "Useful for getting current weather information for a location. "
                "Input should be a place name (e.g., 'Bangalore', 'Paris'). "
                "Returns temperature and precipitation probability."
            )
        )
        
        places_tool = Tool(
            name="PlacesAgent",
            func=self._places_agent_function,
            description=(
                "Useful for getting tourist attractions and places to visit in a location. "
                "Input should be a place name (e.g., 'Bangalore', 'Paris'). "
                "Returns a list of up to 5 tourist attractions."
            )
        )
        
        return [weather_tool, places_tool]


# For testing
if __name__ == "__main__":
    print("Testing LangChain Tools...\n")
    
    tools_factory = TourismTools()
    tools = tools_factory.create_tools()
    
    print(f"✓ Created {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:60]}...")
    
    print("\nTesting Weather Tool:")
    weather_result = tools[0].func("Bangalore")
    print(f"  {weather_result}")
    
    print("\nTesting Places Tool:")
    places_result = tools[1].func("Bangalore")
    print(f"  {places_result}") 