from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="my_app")

# Perform geocoding
location = geolocator.geocode("Oyo State")

# Extract latitude and longitude
latitude = location.latitude
longitude = location.longitude

# Print the result
print(f"Latitude: {latitude}, Longitude: {longitude}")
