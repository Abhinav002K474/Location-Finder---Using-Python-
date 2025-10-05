import phonenumbers
from phonenumbers import geocoder, carrier, NumberParseException
from opencage.geocoder import OpenCageGeocode
import webbrowser

number = "+919080809241"

OPENCAGE_KEY = "92a2ff36e5d84a42a75b76d5e67daffd"

def get_phone_metadata(phonenumber):
    try:
        parsed = phonenumbers.parse(phonenumber)
    except NumberParseException as e:
        raise ValueError(f"Invalid phone number: {e}")
    region = geocoder.description_for_number(parsed, "en") or ""
    provider = carrier.name_for_number(parsed, "en") or ""
    return parsed, region, provider

def geocode_location(query, key):
    geocoder_client = OpenCageGeocode(key)
    results = geocoder_client.geocode(query, limit=1)
    if not results:
        return None
    geom = results[0].get("geometry")
    if not geom or "lat" not in geom or "lng" not in geom:
        return None
    return geom["lat"], geom["lng"]

def open_in_google_maps(lat, lng):
    maps_url = f"https://www.google.com/maps?q={lat},{lng}"
    print(f"📍 Opening in Google Maps: {maps_url}")
    webbrowser.open(maps_url)

def main():
    try:
        parsed, region_text, provider_text = get_phone_metadata(number)
    except ValueError as e:
        print("❌ Error parsing number:", e)
        return

    print("🌍 Region:", region_text)
    print("📡 Carrier:", provider_text)

    if not region_text:
        print("⚠️ Could not detect region.")
        return

    geocode_result = geocode_location(region_text, OPENCAGE_KEY)
    if geocode_result is None:
        print("⚠️ No coordinates found for:", region_text)
        return

    lat, lng = geocode_result
    print("📍 Coordinates:", lat, lng)
    open_in_google_maps(lat, lng)

if __name__ == "__main__":
    main()
