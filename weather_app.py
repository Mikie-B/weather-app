import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import matplotlib.pyplot as plt

print("Welcome to Weather_App")
search_zip = input("Enter a zip code: ")

# Load .env
program_dir = Path(__file__).parent
env_path = program_dir / '.env'
load_dotenv(dotenv_path=env_path)

# API info
api_key=os.getenv("API_KEY")
geocode_url = "http://api.openweathermap.org/geo/1.0/zip"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

# Get latitude and longitude using zip
def geocode_zip(zipcode):
    print(f"Searching {zipcode}...")
    params = {
    "appid":api_key,
    "zip":zipcode
    }
    geocode_response = requests.get(geocode_url,params)
    geocode_data = geocode_response.json()
    return(geocode_data["lat"], geocode_data["lon"])

# Get 5 day forecast in 3 hour increments
def get_forecast(lat,long):
    print(f"Getting forecast for Latitude: {lat}, Longitude: {long}")
    params = {
        "lat": lat,
        "lon": long,
        "appid": api_key,
        "units": "imperial"
    }
    forecast_response = requests.get(forecast_url,params)
    forecast_data = forecast_response.json()
    return forecast_data["list"]


lat, long = geocode_zip(search_zip)
five_day_forecast = get_forecast(lat, long)
datetimes = []
temps = []
for item in five_day_forecast:
    print(f"\nDate: {item["dt_txt"]}")
    print(f"Weather: {item["main"]["temp"]}°F, {item["weather"][0]["description"]}")
    datetime = item["dt_txt"].removesuffix(":00")
    datetimes.append(datetime)
    temps.append(item["main"]["temp"])

plt.plot(datetimes, temps, 'o-')
index = 0
for temp in temps:
    plt.text(datetimes[index],temp,f"{temp}°F")
    index += 1

plt.xticks(rotation=45)
plt.show()