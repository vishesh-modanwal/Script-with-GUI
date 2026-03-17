  


import json
from geopy.geocoders import Nominatim


def get_location(place):
    try:
        geolocator = Nominatim(user_agent="getloc")
        location = geolocator.geocode(place)

        if not location:
            return {"error": "Location not found"}

        return {
            "place": place,
            "address": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "raw_data": location.raw
        }

    except Exception as e:
        return {"error": str(e)}
