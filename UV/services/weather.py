 



import requests
from datetime import datetime
from geopy.geocoders import Nominatim


def iso_to_time(ts):
    return datetime.fromisoformat(ts).strftime("%H:%M:%S")


def get_weather_description(code):
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Cloudy",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        61: "Rain",
        71: "Snow",
        95: "Thunderstorm"
    }
    return weather_map.get(code, "Unknown")


def get_weather_icon(condition):
    condition = condition.lower()

    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "storm" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "fog" in condition:
        return "🌫️"
    else:
        return "🌍"


def get_weather(city):
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)

        if not location:
            return {"error": "Location not found"}

        lat = location.latitude
        lon = location.longitude

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "surface_pressure",
                "wind_speed_10m",
                "cloud_cover",
                "weather_code"
            ],
            "daily": [
                "temperature_2m_min",
                "temperature_2m_max",
                "sunrise",
                "sunset"
            ],
            "hourly": [
                "surface_pressure"
            ],
            "timezone": "auto",
            "forecast_days": 7
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return {"error": "Error fetching weather data"}

        data = response.json()

        description = get_weather_description(data["current"]["weather_code"])

        return {
            "city": city,
            "temperature": data["current"]["temperature_2m"],
            "min_temp": data["daily"]["temperature_2m_min"][0],
            "max_temp": data["daily"]["temperature_2m_max"][0],
            "humidity": data["current"]["relative_humidity_2m"],
            "pressure": data["current"]["surface_pressure"],
            "wind_speed": data["current"]["wind_speed_10m"],
            "cloud_cover": data["current"]["cloud_cover"],
            "sunrise": iso_to_time(data["daily"]["sunrise"][0]),
            "sunset": iso_to_time(data["daily"]["sunset"][0]),
            "latitude": lat,
            "longitude": lon,
            "description": description,
            "forecast_dates": data["daily"]["time"],
            "forecast_min": data["daily"]["temperature_2m_min"],
            "forecast_max": data["daily"]["temperature_2m_max"],
            "pressure_times": data["hourly"]["time"][:12],
            "pressure_values": data["hourly"]["surface_pressure"][:12]
        }

    except Exception as e:
        return {"error": str(e)}