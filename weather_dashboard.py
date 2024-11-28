import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Getting the City’s Coordinates
def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    headers = {"User-Agent": "WeatherDashboard/1.0 (contact@example.com)"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        location_data = response.json()
        if location_data:
            location = location_data[0]
            return float(location['lat']), float(location['lon'])
        else:
            st.warning("City not found. Try adding the country name (e.g., 'Paris, France').")
            return None, None
    else:
        st.error(f"API request failed with status code {response.status_code}: {response.text}")
        return None, None

# Fetching Weather Data with Open-Meteo
def get_weather_data(lat, lon, hours):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&forecast_days=2"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Filter hourly data for the requested hours
        start_index = 0  # Assuming current time aligns with the first entry
        end_index = min(hours, len(data['hourly']['time']))
        filtered_data = {
            "time": data['hourly']['time'][start_index:end_index],
            "temperature_2m": data['hourly']['temperature_2m'][start_index:end_index],
            "relative_humidity_2m": data['hourly']['relative_humidity_2m'][start_index:end_index],
            "wind_speed_10m": data['hourly']['wind_speed_10m'][start_index:end_index],
        }
        return filtered_data
    else:
        st.error("Failed to retrieve weather data.")
        return None

# Building the Streamlit Interface
st.title("Real-Time Weather Dashboard 🌤️")
st.write("Get live weather updates and forecasts.")

city_name = st.text_input("Enter City Name", value="San Francisco")
forecast_duration = st.slider("Select forecast duration (hours)", min_value=12, max_value=48, value=24, step=12)
parameter_options = st.multiselect(
    "Choose weather parameters to display:",
    options=["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)"],
    default=["Temperature (°C)", "Humidity (%)"]
)

# Displaying the Weather Data
if st.button("Get Weather Data"):
    with st.spinner("Fetching weather data..."):
        lat, lon = get_coordinates(city_name)
        if lat and lon:
            data = get_weather_data(lat, lon, forecast_duration)
            if data:
                df = pd.DataFrame({"Time": data['time']})
                df['Time'] = pd.to_datetime(df['Time'])  # Convert to datetime

                if "Temperature (°C)" in parameter_options:
                    df["Temperature (°C)"] = data['temperature_2m']
                    st.subheader("Temperature Forecast")
                    st.line_chart(df.set_index("Time")["Temperature (°C)"])

                if "Humidity (%)" in parameter_options:
                    df["Humidity (%)"] = data['relative_humidity_2m']
                    st.subheader("Humidity Forecast")
                    st.line_chart(df.set_index("Time")["Humidity (%)"])

                if "Wind Speed (m/s)" in parameter_options:
                    df["Wind Speed (m/s)"] = data['wind_speed_10m']
                    st.subheader("Wind Speed Forecast")
                    st.line_chart(df.set_index("Time")["Wind Speed (m/s)"])

                # Adding a Visual Weather Summary
                st.subheader("Current Weather Summary")
                col1, col2, col3 = st.columns(3)
                col1.metric("🌡️ Temperature", f"{data['temperature_2m'][0]}°C")
                col2.metric("💧 Humidity", f"{data['relative_humidity_2m'][0]}%")
                col3.metric("🌬️ Wind Speed", f"{data['wind_speed_10m'][0]} m/s")