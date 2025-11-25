# app.py
import streamlit as st
import pandas as pd
import altair as alt
import os
from PIL import Image
from utils.api import get_current_weather, get_forecast_weather, search_cities

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Vayu - Weather Dashboard",
    page_icon="cloud",
    layout="centered"
)

# === DEFAULT ICON PATH ===
DEFAULT_ICON_PATH = "assets/icons/default.png"

# Ensure default icon exists
if not os.path.exists(DEFAULT_ICON_PATH):
    st.error("Default icon missing! Please add assets/icons/default.png")
    st.stop()

# Load default icon once
DEFAULT_ICON = Image.open(DEFAULT_ICON_PATH)

# === TITLE ===
st.title("Vayu – Your Weather Companion")
st.markdown("### Real-time Current Weather & 5-Day Forecast")

# === SESSION STATE ===
for key in ["selected_city", "show_weather", "last_search"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "show_weather" else False

# === SEARCH ===
search_query = st.text_input(
    "Search for a city:",
    placeholder="e.g., Mumbai, Delhi, Tokyo",
    key="search_input",
    help="Type at least 2 letters"
)

if search_query != st.session_state.last_search:
    st.session_state.show_weather = False
    st.session_state.last_search = search_query

# === AUTOCOMPLETE ===
if search_query and len(search_query) >= 2:
    with st.spinner("Searching..."):
        suggestions = search_cities(search_query)
    if suggestions:
        city_names = [s["name"] for s in suggestions]
        selected = st.selectbox(
            "Select a city:",
            options=[""] + city_names,
            index=0,
            format_func=lambda x: "Choose from suggestions" if not x else x,
            key="city_select"
        )
        if selected:
            st.session_state.selected_city = selected
            st.session_state.show_weather = True
            st.success(f"Selected: **{selected}**")
    else:
        st.warning("No cities found.")
        st.session_state.show_weather = False
else:
    st.session_state.show_weather = False

# === ICON HELPER FUNCTION ===
@st.cache_data(ttl=3600)
def get_icon_with_fallback(icon_url: str):
    """Returns PIL Image with fallback to default cloud"""
    if not icon_url:
        return DEFAULT_ICON
    
    # Fix protocol
    if icon_url.startswith("//"):
        icon_url = "https:" + icon_url

    try:
        import requests
        from io import BytesIO
        response = requests.get(icon_url, timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        pass  # Silently fall back
    return DEFAULT_ICON

# === MAIN DISPLAY ===
if st.session_state.show_weather and st.session_state.selected_city:
    city = st.session_state.selected_city

    placeholder = st.empty()
    with placeholder.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(DEFAULT_ICON, width=140)
        with col2:
            st.markdown("### Loading weather data...")
            st.markdown("#### Please wait...")

    with st.spinner("Fetching weather data..."):
        current_raw = get_current_weather(city)
        forecast_raw = get_forecast_weather(city)

    placeholder.empty()

    if "error" in current_raw:
        st.error(f"Current Weather Error: {current_raw['error']}")
        st.stop()
    if "error" in forecast_raw:
        st.error(f"Forecast Error: {forecast_raw['error']}")
        st.stop()

    # === CURRENT WEATHER ===
    loc = current_raw["location"]
    cur = current_raw["current"]
    city_name = loc["name"]
    region = loc.get("region", "")
    condition = cur["condition"]["text"]
    icon_url = cur["condition"]["icon"]

    st.markdown(f"## {city_name}, {region} • {condition}")

    col1, col2 = st.columns([1, 4])
    with col1:
        icon_img = get_icon_with_fallback(icon_url)
        st.image(icon_img, width=140)
    with col2:
        st.markdown(f"### {cur['temp_c']}°C")
        st.caption(f"Feels like {cur['feelslike_c']}°C")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Humidity", f"{cur['humidity']}%")
    with c2: st.metric("Wind", f"{cur['wind_kph']} kph")
    with c3: st.metric("Feels Like", f"{cur['feelslike_c']}°C")
    with c4: st.metric("Location", f"{city_name}")

    st.markdown("---")

    # === 5-DAY FORECAST ===
    st.subheader("5-Day Forecast")
    forecast_list = forecast_raw["forecast"]["forecastday"]

    for day in forecast_list:
        d = day["day"]
        date_str = day["date"]
        day_name = pd.to_datetime(date_str).strftime("%A")[:3]
        icon_url = d["condition"]["icon"]

        cols = st.columns([1, 2, 3, 2])
        with cols[0]:
            icon_img = get_icon_with_fallback(icon_url)
            st.image(icon_img, width=60)
        with cols[1]:
            st.markdown(f"**{day_name}**")
            st.caption(date_str[5:])
        with cols[2]:
            st.markdown(f"**{d['maxtemp_c']}°** / {d['mintemp_c']}°")
            st.caption(d["condition"]["text"])
        with cols[3]:
            rain = d["daily_chance_of_rain"]
            st.progress(rain / 100)
            st.caption(f"Rain: {rain}%")

    st.markdown("---")

    # === TEMPERATURE CHART (FIXED) ===
    st.subheader("Temperature Trend (5 Days)")

    chart_data = []
    for day in forecast_list:
        date_fmt = pd.to_datetime(day["date"]).strftime("%b %d")
        chart_data.extend([
            {"Date": date_fmt, "Temperature (°C)": day["day"]["maxtemp_c"], "Type": "Max"},
            {"Date": date_fmt, "Temperature (°C)": day["day"]["mintemp_c"], "Type": "Min"},
            {"Date": date_fmt, "Temperature (°C)": day["day"]["avgtemp_c"], "Type": "Avg"}
        ])
    df_chart = pd.DataFrame(chart_data)

    chart = alt.Chart(df_chart).mark_line(point=alt.OverlayMarkDef(size=100)).encode(
        x=alt.X("Date:N", title="Date", sort=None),
        y=alt.Y("Temperature (°C):Q", scale=alt.Scale(zero=False)),
        color=alt.Color("Type:N", legend=alt.Legend(title="Temperature")),
        tooltip=["Date", "Type", "Temperature (°C)"]
    ).properties(height=340).configure_legend(orient="top")

    st.altair_chart(chart, use_container_width=True)

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Refresh All Data"):
            st.rerun()
    with col2:
        if st.button("New Search"):
            for k in ["selected_city", "show_weather", "last_search"]:
                st.session_state[k] = "" if k != "show_weather" else False
            st.rerun()

else:
    st.info("Start typing a city name above to see weather & forecast!")

st.markdown("---")
st.caption("Vayu • Built with love using Streamlit • Powered by WeatherAPI")