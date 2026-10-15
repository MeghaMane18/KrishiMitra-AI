
from fastapi import APIRouter, HTTPException, Query
import requests

router = APIRouter(
    prefix="/weather",
    tags=["Weather and Farming Alerts"]
)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


@router.get("/check")
def check_weather(
    city: str = Query(..., min_length=2, max_length=100)
):
    try:
        # Find the farm's location.
        location_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=15
        )
        location_response.raise_for_status()

        locations = location_response.json().get("results", [])

        if not locations:
            raise HTTPException(
                status_code=404,
                detail="Location not found. Check the village or city name."
            )

        location = locations[0]

        # Fetch current weather and a 3-day forecast.
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "precipitation,weather_code,wind_speed_10m"
                ),
                "daily": (
                    "weather_code,temperature_2m_max,"
                    "temperature_2m_min,precipitation_probability_max,"
                    "precipitation_sum"
                ),
                "forecast_days": 3,
                "timezone": "auto"
            },
            timeout=20
        )
        weather_response.raise_for_status()

        data = weather_response.json()

        return {
            "location": {
                "name": location.get("name", city),
                "admin1": location.get("admin1", ""),
                "country": location.get("country", "")
            },
            "current": data.get("current", {}),
            "daily": data.get("daily", {}),
            "units": {
                "current": data.get("current_units", {}),
                "daily": data.get("daily_units", {})
            },
            "source": "Open-Meteo"
        }

    except HTTPException:
        raise
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Weather service is unavailable. Please try again."
        ) from exc
    except (KeyError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Weather data could not be processed."
        ) from exc
