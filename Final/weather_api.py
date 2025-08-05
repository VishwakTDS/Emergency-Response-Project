import openmeteo_requests
import pandas as pd
import json
import requests
from config import api_key_openWeather

def hourly_weather(lat,long):
	openmeteo = openmeteo_requests.Client()

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": lat,
		"longitude": long,
		"hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "precipitation_probability", "wind_speed_10m", "wind_direction_10m", "visibility"]
	}
	responses = openmeteo.weather_api(url, params=params)
   
	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
	hourly_visibility = hourly.Variables(6).ValuesAsNumpy()

	hourly_data = {"Latitude":response.Latitude(), "Longitude":response.Longitude(),
		"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["precipitation_probability"] = hourly_precipitation_probability
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
	hourly_data["visibility"] = hourly_visibility


	hourly_dataframe = pd.DataFrame(data = hourly_data)
	#print(hourly_dataframe)
	hourly_json = hourly_dataframe.to_json(orient='records')
	return hourly_json

def current_weather(lat,long):
    openmeteo = openmeteo_requests.Client()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
            "latitude": lat,
            "longitude": long,
            "current": ["temperature_2m", "wind_speed_10m", "wind_direction_10m", "precipitation", "relative_humidity_2m", "is_day", "rain", "showers", "snowfall", "cloud_cover", "pressure_msl", "surface_pressure", "weather_code", "apparent_temperature", "wind_gusts_10m"],
            "timezone": "auto"
        }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    current_wind_direction_10m = current.Variables(2).Value()
    current_precipitation = current.Variables(3).Value()
    current_relative_humidity_2m = current.Variables(4).Value()    
    current_is_day = current.Variables(5).Value()
    current_rain = current.Variables(6).Value()
    current_showers = current.Variables(7).Value()
    current_snowfall = current.Variables(8).Value()
    current_cloud_cover = current.Variables(9).Value()
    current_pressure_msl = current.Variables(10).Value()
    current_surface_pressure = current.Variables(11).Value()
    current_weather_code = current.Variables(12).Value()
    current_apparent_temperature = current.Variables(13).Value()
    current_wind_gusts_10m = current.Variables(14).Value()

    current_df = {"Latitude":response.Latitude(), "Longitude":response.Longitude(),"current_temperature_2m":current_temperature_2m,
                    "current_wind_speed_10m":current_wind_speed_10m,
                    "current_wind_direction_10m":current_wind_direction_10m,
                    "current_precipitation":current_precipitation,
                    "current_relative_humidity_2m":current_relative_humidity_2m,
                    "current_is_day":current_is_day,
                    "current_rain":current_rain,
                    "current_showers":current_showers,
                    "current_snowfall":current_snowfall,
                    "current_cloud_cover":current_cloud_cover,
                    "current_pressure_msl":current_pressure_msl,
                    "current_surface_pressure":current_surface_pressure,
                    "current_weather_code":current_weather_code,
                    "current_apparent_temperature":current_apparent_temperature,
                    "current_wind_gusts_10m":current_wind_gusts_10m
                    }

    current_json = json.dumps(current_df)
    return current_json


def get_location(lat, lon):
    api_key = api_key_openWeather
    if not api_key:
        raise ValueError("An OpenWeatherMap API key must be provided.")

    url = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "APPID": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        return {}

    loc = data[0]
    return ", ".join(filter(None, [loc.get("name"), loc.get("state"), loc.get("country")]))
