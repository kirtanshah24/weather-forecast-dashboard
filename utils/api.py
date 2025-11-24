# utils/api.py
import requests
import streamlit as st
import time
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1"


# === SEARCH CITIES ===
def search_cities(query: str, limit: int = 6):
    if not query or len(query.strip()) < 2:
        return []
    if not _is_valid_input(query):
        return []

    url = f"{BASE_URL}/search.json"
    params = {"key": API_KEY, "q": query.strip()}

    return _make_request(url, params, is_search=True)[:limit]


# === CURRENT WEATHER ===
def get_current_weather(city: str):
    if not city or not _is_valid_input(city):
        return {"error": "Invalid city name. Use letters and spaces only."}

    url = f"{BASE_URL}/current.json"
    params = {"key": API_KEY, "q": city.strip()}

    return _make_request(url, params)


# === PRIVATE HELPERS ===
def _is_valid_input(text: str) -> bool:
    import re
    return bool(re.match(r"^[a-zA-Z\s,\-\.]+$", text.strip()))


def _make_request(url: str, params: dict, is_search: bool = False, retries: int = 2):
    """Centralized request with retry, timeout, rate limit handling"""

    # Safety: Missing API key
    if not API_KEY:
        return {"error": "Missing API key. Set WEATHER_API_KEY in Streamlit Secrets."}

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json() if is_search else _parse_current_weather(response.json())

            elif response.status_code == 429:
                wait = 2 ** attempt
                if attempt < retries:
                    time.sleep(wait)
                    continue
                return {"error": "Rate limit exceeded. Please try again in a minute."}

            elif response.status_code == 400:
                msg = response.json().get("error", {}).get("message", "Bad request")
                return {"error": msg}

            else:
                return {"error": f"API error: {response.status_code}"}

        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(1)
                continue
            return {"error": "Request timed out. Check your internet."}

        except requests.exceptions.ConnectionError:
            return {"error": "No internet connection."}

        except Exception:
            return {"error": "Something went wrong. Please try again."}

    return {"error": "Failed after multiple attempts."}


def _parse_current_weather(data: dict) -> dict:
    """Safely extract weather data from API response"""
    try:
        return {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temp_c": data["current"]["temp_c"],
            "feels_like_c": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"]
        }
    except KeyError:
        return {"error": "Incomplete data from API."}
