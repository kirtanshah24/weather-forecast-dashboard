import pytest
from utils.api import get_current_weather, search_cities


def test_search_cities_success(requests_mock):
    """Test successful city search API call."""

    mock_response = [
        {"name": "Mumbai"},
        {"name": "Mumbai City"}
    ]

    requests_mock.get(
        "https://api.weatherapi.com/v1/search.json",
        json=mock_response,
        status_code=200
    )

    result = search_cities("Mumbai")

    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["name"] == "Mumbai"


def test_get_current_weather_success(requests_mock):
    """Test normalized formatted weather response."""

    mock_response = {
        "location": {"name": "London", "region": "London"},
        "current": {
            "temp_c": 20,
            "feelslike_c": 19,
            "humidity": 60,
            "wind_kph": 10,
            "condition": {
                "text": "Cloudy",
                "icon": "//cdn.weatherapi.com/icon.png"
            }
        }
    }

    requests_mock.get(
        "https://api.weatherapi.com/v1/current.json",
        json=mock_response,
        status_code=200
    )

    weather = get_current_weather("London")

    assert isinstance(weather, dict)
    assert weather["city"] == "London"
    assert weather["temp_c"] == 20
    assert weather["condition"] == "Cloudy"
    assert "icon" in weather


def test_get_current_weather_invalid_city(requests_mock):
    """Test graceful handling of invalid location."""

    requests_mock.get(
        "https://api.weatherapi.com/v1/current.json",
        status_code=400,
        json={"error": {"message": "No matching location found"}}
    )

    weather = get_current_weather("InvalidCity")

    assert "error" in weather
    assert weather["error"] == "No matching location found"
