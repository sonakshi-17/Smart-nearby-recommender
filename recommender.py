from api import get_places

def recommend_places(location, mood):

    mood_map = {
        "Work": "cafe",
        "Date": "restaurant",
        "Quick Bite": "fast_food",
        "Budget": "restaurant"
    }

    place_type = mood_map.get(mood)

    results = get_places(location, place_type)

    # Fallback if API returns nothing
    if not results:
        return [
            {
                "name": "Nearby Cafe",
                "area": location,
                "address": "Local area",
                "cost": "₹400 - ₹800 for two"
            },
            {
                "name": "Popular Restaurant",
                "area": location,
                "address": "Main street",
                "cost": "₹800 - ₹1500 for two"
            }
        ]

    return results