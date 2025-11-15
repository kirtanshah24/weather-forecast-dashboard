# app.py
import streamlit as st
from utils.api import get_current_weather, search_cities

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Vayu - Weather Dashboard",
    page_icon="cloud",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === TITLE ===
st.title("cloud Vayu")
st.subheader("Real-time Weather Dashboard")

# === SESSION STATE ===
for key in ["selected_city", "show_weather", "last_search"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "show_weather" else False

# === SEARCH INPUT ===
search_query = st.text_input(
    "Search for a city:",
    placeholder="e.g., Mumbai, London, Tokyo",
    key="search_input",
    help="Type at least 2 letters"
)

# Reset on new search
if search_query != st.session_state.last_search:
    st.session_state.show_weather = False
    st.session_state.last_search = search_query

# === AUTOCOMPLETE ===
if search_query and len(search_query) >= 2:
    with st.spinner("Searching cities..."):
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
        st.warning("No cities found. Try another name.")
        st.session_state.show_weather = False
else:
    st.session_state.show_weather = False

# === WEATHER DISPLAY (ONLY ON SELECTION) ===
if st.session_state.show_weather and st.session_state.selected_city:
    city = st.session_state.selected_city

    # Loading skeleton
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("<div style='width:120px; height:120px; background:#f0f0f0; border-radius:12px;'></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("### Loading city...")
            st.markdown("#### Loading condition...")

    with st.spinner(f"Fetching weather for **{city}**..."):
        weather_data = get_current_weather(city)

    # Clear skeleton
    st.empty()

    if "error" not in weather_data:
        # SUCCESS
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(weather_data["icon"], width=120)
        with col2:
            st.markdown(f"""
            ### {weather_data['city']}, {weather_data['region']}
            #### {weather_data['condition']}
            """)

        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Temperature", f"{weather_data['temp_c']}°C")
        with m2: st.metric("Feels Like", f"{weather_data['feels_like_c']}°C")
        with m3: st.metric("Humidity", f"{weather_data['humidity']}%")

        m4, m5 = st.columns(2)
        with m4: st.metric("Wind", f"{weather_data['wind_kph']} kph")
        with m5: st.caption("Data from WeatherAPI")

        if st.button("Refresh"):
            st.rerun()

    else:
        # ERROR HANDLING
        error = weather_data["error"]
        if "rate limit" in error.lower():
            st.error("Rate limit exceeded. Please try again in a minute.")
        elif "internet" in error.lower():
            st.error("No internet connection. Check your network.")
        elif "invalid" in error.lower():
            st.error("Invalid city name. Use letters only.")
        else:
            st.error(f"Error: {error}")

        st.session_state.show_weather = False

    if st.button("Clear Search"):
        for k in ["selected_city", "show_weather", "last_search"]:
            st.session_state[k] = "" if k != "show_weather" else False
        st.rerun()

else:
    st.info("Start typing → Select a city from dropdown to see weather!")

# === FOOTER ===
st.markdown("---")
st.caption("Built with love using Streamlit • Powered by WeatherAPI")