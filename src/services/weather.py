"""
Weather Service - Open-Meteo API Integration
Fetches current weather and forecast data.
"""

import requests
from typing import Optional, Dict


class WeatherService:
    """Handles weather data retrieval using Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_weather(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Get current weather for given coordinates.
        
        Args:
            latitude: Geographic latitude
            longitude: Geographic longitude
            
        Returns:
            Dict with 'temperature' and 'precipitation_probability' or None
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "hourly": "precipitation_probability",
            "forecast_days": 1
        }
        
        try:
            response = self.session.get(
                self.BASE_URL, 
                params=params, 
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current_weather", {})
            hourly = data.get("hourly", {})
            
            # Get current hour's precipitation probability
            precip_probs = hourly.get("precipitation_probability", [0])
            current_precip = precip_probs[0] if precip_probs else 0
            
            return {
                "temperature": current.get("temperature"),
                "precipitation_probability": current_precip,
                "windspeed": current.get("windspeed", 0),
                "weathercode": current.get("weathercode", 0)
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Weather API error: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Error parsing weather response: {e}")
            return None
    
    def format_weather_description(self, weather_data: Dict) -> str:
        """Format weather data into human-readable description"""
        temp = weather_data.get("temperature")
        precip = weather_data.get("precipitation_probability", 0)
        
        return f"it's currently {temp}°C with a chance of {precip}% to rain"


# For testing
if __name__ == "__main__":
    service = WeatherService()
    
    # Test with Bangalore coordinates
    print("Testing Weather API...")
    print("Location: Bangalore (12.9716, 77.5946)\n")
    
    weather = service.get_weather(12.9716, 77.5946)
    if weather:
        print(f"✓ Temperature: {weather['temperature']}°C")
        print(f"✓ Precipitation: {weather['precipitation_probability']}%")
        print(f"✓ Wind Speed: {weather['windspeed']} km/h")
        print(f"\nFormatted: {service.format_weather_description(weather)}")
    else:
        print("✗ Failed to fetch weather")