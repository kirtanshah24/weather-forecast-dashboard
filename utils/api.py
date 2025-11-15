# utils/api.py
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1"

def get_current_weather(city: str):
    """
    Fetch current weather for a city using WeatherAPI
    Returns dict with weather data or None if error
    """
    if not city.strip():
        return None

    url = f"{BASE_URL}/current.json"
    params = {
        "key": API_KEY,
        "q": city.strip()
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["location"]["name"],
                "region": data["location"]["region"],
                "country": data["location"]["country"],
                "temp_c": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "wind_kph": data["current"]["wind_kph"],
                "condition": data["current"]["condition"]["text"],
                "icon": f"https:{data['current']['condition']['icon']}",
                "feels_like_c": data["current"]["feelslike_c"]
            }
        else:
            error_msg = response.json().get("error", {}).get("message", "Unknown error")
            return {"error": error_msg}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}