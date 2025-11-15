# app.py
import streamlit as st
from utils.api import get_current_weather, search_cities

# Page config
st.set_page_config(
    page_title="Vayu - Weather Dashboard",
    page_icon="cloud",
    layout="centered"
)

# Title
st.title("cloud Vayu")
st.subheader("Real-time Weather Dashboard")

# Initialize session state
if "selected_city" not in st.session_state:
    st.session_state.selected_city = ""
if "show_weather" not in st.session_state:
    st.session_state.show_weather = False

# Search input
search_query = st.text_input(
    "Search for a city:",
    placeholder="Type city name (e.g., Mumbai, Lon, New York)",
    key="search_input"
)

# Reset weather when new search starts
if search_query != st.session_state.get("last_search", ""):
    st.session_state.show_weather = False
    st.session_state.last_search = search_query

# Show autocomplete only if typing 2+ chars
if search_query and len(search_query) >= 2:
    with st.spinner("Searching cities..."):
        suggestions = search_cities(search_query, limit=6)

    if suggestions:
        city_names = [s["name"] for s in suggestions]
        selected = st.selectbox(
            "Select a city:",
            options=[""] + city_names,  # Add empty option at top
            index=0,
            format_func=lambda x: "↓ Choose from suggestions" if x == "" else x,
            key="city_select"
        )

        # Only trigger weather when user selects a real city
        if selected and selected != "":
            st.session_state.selected_city = selected
            st.session_state.show_weather = True
            st.success(f"Selected: **{selected}**")
    else:
        st.warning("No cities found. Try another name.")
        st.session_state.show_weather = False
else:
    st.session_state.show_weather = False

# === ONLY SHOW WEATHER IF USER SELECTED A CITY FROM DROPDOWN ===
if st.session_state.show_weather and st.session_state.selected_city:
    city_to_fetch = st.session_state.selected_city

    with st.spinner(f"Fetching weather for **{city_to_fetch}**..."):
        weather_data = get_current_weather(city_to_fetch)

    if weather_data and "error" not in weather_data:
        # Success - Display weather
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(weather_data["icon"], width=120)
        with col2:
            st.markdown(f"""
            ### {weather_data['city']}, {weather_data['region']}
            #### {weather_data['condition']}
            """)

        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Temperature", f"{weather_data['temp_c']}°C")
        with m2:
            st.metric("Feels Like", f"{weather_data['feels_like_c']}°C")
        with m3:
            st.metric("Humidity", f"{weather_data['humidity']}%")

        m4, m5 = st.columns(2)
        with m4:
            st.metric("Wind", f"{weather_data['wind_kph']} kph")
        with m5:
            st.caption("Data from WeatherAPI")

        # Refresh button
        if st.button("Refresh Data"):
            st.rerun()

    elif weather_data and "error" in weather_data:
        st.error(f"Error: {weather_data['error']}")
        st.session_state.show_weather = False
    else:
        st.warning("No data received.")
        st.session_state.show_weather = False

else:
    st.info("Start typing a city name → Select from dropdown to see weather!")

# Clear button
if st.session_state.show_weather:
    if st.button("Clear Search"):
        st.session_state.selected_city = ""
        st.session_state.show_weather = False
        st.rerun()

# Footer
st.markdown("---")
st.caption("Built with love using Streamlit | Powered by WeatherAPI")