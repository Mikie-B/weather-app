import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import matplotlib.pyplot as plt
import customtkinter
import datetime

customtkinter.set_default_color_theme('dark-blue')
customtkinter.set_appearance_mode('Dark')

print("Welcome to Weather_App")
today = datetime.date.today()

# Load .env
program_dir = Path(__file__).parent
env_path = program_dir / '.env'
load_dotenv(dotenv_path=env_path)

# API info
api_key=os.getenv("API_KEY")
geocode_url = "http://api.openweathermap.org/geo/1.0/zip"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
current_weather_url = "https://api.openweathermap.org/data/2.5/weather"

# Get latitude and longitude using zip
def geocode_zip(zipcode):
    print(f"Searching {zipcode}...")
    params = {
    "appid":api_key,
    "zip":zipcode
    }
    geocode_response = requests.get(geocode_url,params)
    geocode_data = geocode_response.json()
    return(geocode_data["lat"], geocode_data["lon"], geocode_data["name"])

# Get 5 day forecast in 3 hour increments
def get_5d3h_forecast(lat,long):
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

def get_current_weather(lat, long):
    print(f"Getting current weather conditions for Latitude: {lat}, Longitude: {long}")
    params = {
        "lat": lat,
        "lon": long,
        "appid": api_key,
        "units": "imperial"
    }
    current_weather_response = requests.get(current_weather_url, params)
    current_weather_data = current_weather_response.json()
    return current_weather_data

def search(zip):
    global lat, long, city
    try:
        lat, long, city = geocode_zip(zipcode=zip)
    except:
        print(f"ZIP code not found: {zip}")
    global current_weather 
    current_weather = get_current_weather(lat, long)

class current_weather_frame(customtkinter.CTkFrame):
    def __init__(self, master, conditions, temp, high, low, search_zip):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        self.currentdate = customtkinter.CTkLabel(self.frame, text = f"{today.strftime("%B %d, %Y")}", text_color="white", font=("Arial", 16))
        self.currentdate.pack(padx=100, pady=50)
        self.location = customtkinter.CTkLabel(self.frame, text=f"Location: {city}", text_color="white", font=("Arial", 16))
        self.location.pack()
        self.currentcondition = customtkinter.CTkLabel(self.frame,text=f"Conditions: {conditions}", text_color="white", font=("Arial", 16))
        self.currentcondition.pack()
        self.currenttemp = customtkinter.CTkLabel(self.frame,text=f"Temperature: {temp}\u00b0F", text_color="white", font=("Arial", 16))
        self.currenttemp.pack()
        self.high = customtkinter.CTkLabel(self.frame, text=f"High: {high}\u00b0F", text_color="white", font=("Arial", 16))
        self.high.pack()
        self.low = customtkinter.CTkLabel(self.frame, text=f"Low: {low}\u00b0F", text_color="white", font=("Arial", 16))
        self.low.pack()
        self.searchbutton = customtkinter.CTkButton(self.frame, text="Search", command=self.button_callback)
        self.searchbutton.pack(side="bottom", pady=50)
        self.zipentry = customtkinter.CTkTextbox(self.frame, height=20)
        self.zipentry.pack(side="bottom")
        self.zipentry.insert("0.0", search_zip)
        self.ziplabel = customtkinter.CTkLabel(self.frame, text="ZIP Code",text_color="white", font=("Arial", 16))
        self.ziplabel.pack(side="bottom")

        
    def button_callback(self):
        zip=self.zipentry.get("0.0", "end").strip()
        if len(zip) == 5 and zip.isdigit():
            search(zip)
            try:
                self.location.configure(text=f"Location: {city}")
                self.currentcondition.configure(text=f"Conditions: {current_weather['weather'][0]['main']}")
                self.currenttemp.configure(text=f"Temperature: {current_weather['main']['temp']}\u00b0F")
                self.high.configure(text=f"High: {current_weather['main']['temp_max']}\u00b0F")
                self.low.configure(text=f"Low: {current_weather['main']['temp_min']}\u00b0F")
                print("Labels updated")
            except Exception as e:
                print("Failed to update labels:", e)
        else:
            print("Enter a valid ZIP code")

class Window(customtkinter.CTk):
    def __init__(self, conditions, temp, high, low, search_zip):
        super().__init__()

        self.geometry('500x600')
        self.title("Weather App")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        cw = current_weather_frame(master=self, conditions=conditions, temp=temp, high=high, low=low, search_zip=search_zip)
        cw.grid(row=0, column=0, sticky="ns", pady=10)

city=""

window = Window(conditions="", 
                temp="", 
                high="", 
                low="",
                search_zip="")
window.mainloop()