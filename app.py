import requests
import pandas as pd
import json
import streamlit as st
from streamlit_folium import folium_static
from streamlit.components.v1 import html
import os
import sys
import time
import datetime as dt
import pytz
# Scientific libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from geopy.geocoders import Nominatim

from keys import MAP_TOKEN, CLIMACELL_API, WEATHER_API
from PIL import Image
from datetime import datetime, timedelta
from copy import deepcopy


from mapbox import Geocoder
import folium
from streamlit_option_menu import option_menu

MAP_TOKEN_API = MAP_TOKEN
CLIMACELL_API = CLIMACELL_API
WEATHER = WEATHER_API

st.set_page_config(layout='centered')

st.image('weather.jpg', width=300)

st.title('Mini Rain Predictor🌧️')



st.title("Rainfall Prediction")

# Sidebar content
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Rain Prediction", "About"],
                    icons= ["🏠", "🌧️", "📝"], menu_icon="cast", default_index=1)
    selected

if selected == "About":
    st.markdown("## About")
    st.markdown("This app predicts the probability of rain for seven days in a given location. It uses the [Climacell API](https://www.climacell.co/weather-api/) to get the weather data and [Streamlit](https://streamlit.io/) to display the results. Enter the desired city using the search bar and get the results! The following dataframe shows the cities that are available in the API:")

# Input search components
# state = st.text_input("Enter state:")
city = st.text_input("Enter city  (ex: Albany, NY):")



if city:
    geocoder = Geocoder(access_token=MAP_TOKEN_API)
    response = geocoder.forward(city, limit=1)
    features = response.json()['features']

    if features:
        coordinates = features[0]['geometry']['coordinates']
        st.write(f"Coordinates: {coordinates}")


# Get the area code for the given city
# def get_area_code(city):

    


# Get the weather data for the given city
def get_weather_data(city):
    geolocator = Nominatim(user_agent="weather_app")

    # Get geolocation data for city
    geolocation = geolocator.geocode(city)




    if geolocation is not None:
        # Get latitude and longitude of the city
        latitude = geolocation.latitude
        longitude = geolocation.longitude

        url = f"https://api.weather.gov/points/{latitude},{longitude}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            handle_response(data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching weather data: {e}")
            return None
    else:
        raise ValueError("Geolocation not found for the given city.")


# Extract data for city
def handle_response(data):

    try:
      periods = data['properties']['periods']

      for period in periods:
         temperature = period['temperature']
         description = period['shortForecast']
         start_time = period['startTime']
         end_time = period['endTime']
    
    except KeyError:
        print("Error occurred while fetching weather data.")
        return None

  # Display or process the data as needed
        print(f"Temperature: {temperature}")
        print(f"Description: {description}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")

if st.button("Search"):
    weather_data = get_weather_data(city)
    if weather_data is not None:
        st.write(weather_data)

# Call the API

def fetch_forecast(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        periods = data['properties']['periods']
        forecast_temperature = []

        for period in periods:
            temperature = period['temperature']
            forecast_temperature.append(temperature)

        return forecast_temperature
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching weather data: {e}")
        return None

# Display the modified DataFrame

#get coordinates data 



# Search 
def search_location(query):
    geocoder = Geocoder(access_token=MAP_TOKEN_API)
    response = geocoder.forward(query)
    features = response.json()['features']


    if not features:
        print("No results found")
    return features

with open('mapbox.js') as f:
    js = f.read()

html(js, height=0)
def get_coordinates(features):  
    # Get the coordinates of the first result
    coordinates = features[0]['geometry']['coordinates']
    return coordinates



## dataframe for us cities

cities = pd.read_csv('uscities.csv')
cities.rename(columns={'lat':'latitude'} , inplace=True)
cities.rename(columns={'lng':'longitude'} , inplace=True)

filtered_cities = cities[cities['city'].str.contains(city, case=False)]



    
location = search_location(city)


filtered_cities = cities[cities['city'].str.contains(city, case=False) | cities['state_id'].str.contains(city, case=False)]


# Display the map

if city: 

    m = folium.Map(location=get_coordinates(location), zoom_start=12, tiles='OpenStreetMap', API=MAP_TOKEN_API)
    folium.Marker(location=get_coordinates(location), popup=city).add_to(m)
    st.write(f"Map of: {city}")
    folium_static(m)
    








# Get the forecast data (Albany, NY)
forecast_url = f"https://api.weather.gov/zone/forecast/{city}/forecast"


## Get lightning data for location chosen:
lightning_url = f"https://api.weather.gov/products/types/LightningData/locations/{city}/time"


st.markdown('Made with ❤️ by Lynette Okoth || See other projects at [Github](https://github.com/lyokoth/)')
