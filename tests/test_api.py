import pytest
from utils.api import get_current_weather, search_cities

TEST_KEY = "TEST_KEY"

def test_search_cities_success(requests_mock):
    mock_response = [
        {"name": "Mumbai"},
        {"name": "Mumbai City"}
    ]

    requests_mock.get(
        f"https://api.weatherapi.com/v1/search.json?key={TEST_KEY}&q=Mumbai",
        json=mock_response,
        status_code=200
    )

    result = search_cities("Mumbai")
    assert isinstance(result, list)
    assert result[0]["name"] == "Mumbai"


def test_get_current_weather_success(requests_mock):
    mock_response = {
        "location": {"name": "London", "region": "London"},
        "current": {
            "temp_c": 20,
            "feelslike_c": 19,
            "humidity": 60,
            "wind_kph": 10,
            "condition": {"text": "Cloudy", "icon": "//cdn.weatherapi.com/icon.png"}
        }
    }

    requests_mock.get(
        f"https://api.weatherapi.com/v1/current.json?key={TEST_KEY}&q=London",
        json=mock_response,
        status_code=200
    )

    weather = get_current_weather("London")
    assert weather["city"] == "London"
    assert weather["temp_c"] == 20
    assert weather["condition"] == "Cloudy"


def test_get_current_weather_invalid_city(requests_mock):
    requests_mock.get(
        f"https://api.weatherapi.com/v1/current.json?key={TEST_KEY}&q=InvalidCity",
        status_code=400,
        json={"error": {"message": "No matching location found"}}
    )

    weather = get_current_weather("InvalidCity")
    assert "error" in weather
