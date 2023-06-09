import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests

# Load a dataframe with the beaches of Euskadi
playas_df = pd.read_excel("espacios_naturales1.xlsx")
beach_coordinates = playas_df.loc[:, ["LATWGS84", "LONWGS84"]]

# Get user location
user_lat = float(input("Please enter your latitude: "))
user_lon = float(input("Please enter your longitude: "))

# Calculate the distance between two points
def geodesic_distance(lat1, lon1, lat2, lon2):
    start = (lat1, lon1)
    end = (lat2, lon2)
    distance = geodesic(start, end).km
    return distance

# Compute distances to beaches
beach_distances = beach_coordinates.apply(lambda row: geodesic_distance(user_lat, user_lon, row["LATWGS84"], row["LONWGS84"]), axis=1)
coordinadas_pd = pd.concat([playas_df["PLAYA"], beach_distances], axis=1)
coordinadas_pd.columns = ["Beach", "Distance to User (km)"]

# Find nearest beach
nearest_beach_info = coordinadas_pd.loc[coordinadas_pd["Distance to User (km)"].idxmin()]
nearest_beach = nearest_beach_info["Beach"]
nearest_beach_distance = nearest_beach_info["Distance to User (km)"]

# Print the nearest beach and the distance to the user
print("The nearest beach is", nearest_beach, "and it is", nearest_beach_distance, "km away.")

# Get weather data
def get_weather_data():
    start_date = input("Please enter the start date (YYYY-MM-DD): ")
    end_date = input("Please enter the end date (YYYY-MM-DD): ")
    url = f"https://api.meteomatics.com/{start_date}T00:00:00Z--{end_date}T00:00:00Z:PT1H/t_2m:C/{user_lat},{user_lon}/html"
    params = {
        "apikey": "Your API Key"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.text
    else:
        return None

start_date = input("Please enter the start date (YYYY-MM-DD): ")
end_date = input("Please enter the end date (YYYY-MM-DD): ")

weather_data = get_weather_data()

if weather_data is not None:
    print(weather_data)
else:
    print("Failed to retrieve weather data.")

