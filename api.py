import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "SmartNearbyRecommenderApp"
}

def get_places(location, mood_type):

    try:
        # Step 1: Convert location to lat-long
        geo_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
        geo_response = requests.get(geo_url, headers=HEADERS).json()

        if not geo_response:
            return []

        lat = geo_response[0]['lat']
        lon = geo_response[0]['lon']

        radius = 2000

        query = f"""
        [out:json];
        (
          node["amenity"="{mood_type}"](around:{radius},{lat},{lon});
          way["amenity"="{mood_type}"](around:{radius},{lat},{lon});
          relation["amenity"="{mood_type}"](around:{radius},{lat},{lon});
        );
        out center tags;
        """

        response = requests.post(OVERPASS_URL, data=query, headers=HEADERS).json()

        if "elements" not in response:
            return []

        places = []

        for place in response["elements"][:8]:

            tags = place.get("tags", {})

            name = tags.get("name", "Unknown")

            address = ", ".join(filter(None, [
                tags.get("addr:street"),
                tags.get("addr:city"),
                tags.get("addr:postcode")
            ]))

            area = tags.get("addr:suburb") or tags.get("addr:city") or "Nearby"

            if mood_type == "restaurant":
                cost = "₹800 - ₹1500 for two"
            elif mood_type == "cafe":
                cost = "₹400 - ₹800 for two"
            elif mood_type == "fast_food":
                cost = "₹200 - ₹500 for two"
            else:
                cost = "₹300 - ₹700 for two"

            places.append({
                "name": name,
                "area": area,
                "address": address if address else "Address not available",
                "cost": cost
            })

        return places

    except:
        return []