import os
import requests
import time
import os
import pandas as pd
from typing import List, Dict

# Hardcoded API key (as per your choice)
API_KEY = "619f0dea8fc24a38beb115843251211"
BASE_URL = "http://api.weatherapi.com/v1"

# Simple in-memory cache to reduce API calls
_cache = {}

def search_cities(query: str, limit: int = 6) -> List[Dict]:
    if not query or len(query.strip()) < 2 or not _is_valid_input(query):
        return []

    cache_key = f"search_{query.strip().lower()}"
    if cache_key in _cache:
        return _cache[cache_key]

    url = f"{BASE_URL}/search.json"
    params = {"key": API_KEY, "q": query.strip()}

    result = _make_request(url, params, is_search=True)
    _cache[cache_key] = result[:limit] if isinstance(result, list) else []
    return _cache[cache_key]

def get_current_weather(city: str) -> Dict:
    if not city or not _is_valid_input(city):
        return {"error": "Invalid city name."}

    cache_key = f"current_{city.lower()}"
    if cache_key in _cache:
        return _cache[cache_key]

    url = f"{BASE_URL}/current.json"
    params = {"key": API_KEY, "q": city.strip()}
    result = _make_request(url, params)
    _cache[cache_key] = result
    return result

def get_forecast_weather(city: str, days: int = 5) :
    """Returns 5-day forecast with daily summary"""
    if not city or not _is_valid_input(city):
        return {"error": "Invalid city name."}

    cache_key = f"forecast_{city.lower()}"
    if cache_key in _cache:
        return _cache[cache_key]

    url = f"{BASE_URL}/forecast.json"
    params = {"key": API_KEY, "q": city.strip(), "days": days}

    raw = _make_request(url, params)
    _cache[cache_key] = raw
    return raw

    try:
        forecast_days = []
        for day in raw["forecast"]["forecastday"]:
            d = day["day"]
            forecast_days.append({
                "date": day["date"],
                "day_name": pd.to_datetime(day["date"]).strftime("%A"),
                "max_temp": d["maxtemp_c"],
                "min_temp": d["mintemp_c"],
                "avg_temp": d["avgtemp_c"],
                "condition": d["condition"]["text"],
                "icon": d["condition"]["icon"],
                "humidity": d["avghumidity"],
                "chance_of_rain": d["daily_chance_of_rain"]
            })
        result = {"forecast": forecast_days}
        _cache[cache_key] = result
        return result
    except Exception:
        return {"error": "Failed to parse forecast data."}

# === PRIVATE HELPERS ===
def _is_valid_input(text: str) -> bool:
    import re
    return bool(re.match(r"^[a-zA-Z\s,\-\.]+$", text.strip()))

def _make_request(url: str, params: dict, is_search: bool = False, retries: int = 2):
    if not API_KEY:
        return {"error": "API key missing."}

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=12)
            if response.status_code == 200:
                return response.json() if is_search else response.json()
            elif response.status_code == 429:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                return {"error": "Rate limit exceeded. Try again later."}
            elif response.status_code == 400:
                msg = response.json().get("error", {}).get("message", "Invalid location")
                return {"error": msg}
            else:
                return {"error": f"API error {response.status_code}"}
        except requests.exceptions.RequestException:
            if attempt == retries:
                return {"error": "Network error. Check your internet."}
            time.sleep(1)
    return {"error": "Request failed."}

def _parse_current_weather(data: dict) -> dict:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "temp_c": data["current"]["temp_c"],
            "feels_like_c": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"]
        }
    except KeyError:
        return {"error": "Incomplete weather data."}
