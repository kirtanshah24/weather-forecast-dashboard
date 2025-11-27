# # app.py
# import streamlit as st
# import pandas as pd
# import altair as alt
# from utils.api import get_current_weather, get_forecast_weather, search_cities

# # === PAGE CONFIG ===
# st.set_page_config(
#     page_title="Vayu - Weather Dashboard",
#     page_icon="cloud",
#     layout="centered"
# )

# # === TITLE ===
# st.title("Vayu – Your Weather Companion")
# st.markdown("### Real-time Current Weather & 5-Day Forecast")

# # === SESSION STATE ===
# for key in ["selected_city", "show_weather", "last_search"]:
#     if key not in st.session_state:
#         st.session_state[key] = "" if key != "show_weather" else False

# # === SEARCH ===
# search_query = st.text_input(
#     "Search for a city:",
#     placeholder="e.g., Mumbai, Delhi, Tokyo",
#     key="search_input",
#     help="Type at least 2 letters"
# )

# if search_query != st.session_state.last_search:
#     st.session_state.show_weather = False
#     st.session_state.last_search = search_query

# # === AUTOCOMPLETE ===
# if search_query and len(search_query) >= 2:
#     with st.spinner("Searching..."):
#         suggestions = search_cities(search_query)
#     if suggestions:
#         city_names = [s["name"] for s in suggestions]
#         selected = st.selectbox(
#             "Select a city:",
#             options=[""] + city_names,
#             index=0,
#             format_func=lambda x: "Choose from suggestions" if not x else x,
#             key="city_select"
#         )
#         if selected:
#             st.session_state.selected_city = selected
#             st.session_state.show_weather = True
#             st.success(f"Selected: **{selected}**")
#     else:
#         st.warning("No cities found.")
#         st.session_state.show_weather = False
# else:
#     st.session_state.show_weather = False

# # === MAIN WEATHER DISPLAY ===
# if st.session_state.show_weather and st.session_state.selected_city:
#     city = st.session_state.selected_city

#     # Skeleton
#     placeholder = st.empty()
#     with placeholder.container():
#         col1, col2 = st.columns([1, 4])
#         with col1:
#             st.markdown("<div style='width:140px;height:140px;background:#eee;border-radius:50%;'></div>", unsafe_allow_html=True)
#         with col2:
#             st.markdown("### Loading weather data...")
#             st.markdown("#### Please wait...")

#     # Fetch data
#     with st.spinner("Fetching current & forecast data..."):
#         current_raw = get_current_weather(city)      # ← raw response
#         forecast_raw = get_forecast_weather(city)    # ← raw response

#     placeholder.empty()

#     # === CHECK FOR ERRORS ===
#     if "error" in current_raw:
#         st.error(f"Current Weather Error: {current_raw['error']}")
#         st.stop()
#     if "error" in forecast_raw:
#         st.error(f"Forecast Error: {forecast_raw['error']}")
#         st.stop()

# #     # === EXTRACT CURRENT WEATHER ===
# # === EXTRACT CURRENT WEATHER ===
#     city_name = current_raw["city"]
#     region = current_raw["region"]
#     temp_c = current_raw["temp_c"]
#     # feels_like = current_raw["feels_like"]
#     humidity = current_raw["humidity"]
#     wind_kph = current_raw["wind_kph"]
#     condition = current_raw["condition"]
    
#     icon_url = (
#         "https:" + current_raw["icon"]
#         if current_raw["icon"].startswith("//")
#         else current_raw["icon"]
#     )


    
# #     # loc = current_raw["location"]
# #     # cur = current_raw["current"]

# #     city_name = current_raw["city"]
# # region = current_raw["region"]
# # temp_c = current_raw["temp_c"]
# # condition = current_raw["condition"]
# # icon_url = "https:" + current_raw["icon"]


# #     city_name = loc["name"]
# #     region = loc.get("region", "")
# #     country = loc["country"]
# #     temp_c = cur["temp_c"]
# #     feels_like = cur["feelslike_c"]
# #     humidity = cur["humidity"]
# #     wind_kph = cur["wind_kph"]
# #     condition = cur["condition"]["text"]
# #     icon_url = "https:" + cur["condition"]["icon"] if cur["condition"]["icon"].startswith("//") else cur["condition"]["icon"]

#     # === DISPLAY CURRENT WEATHER ===
#     st.markdown(f"## {city_name}, {region} • {condition}")

#     col1, col2 = st.columns([1, 4])
#     with col1:
#         st.image(icon_url, width=140)
#     with col2:
#         st.markdown(f"### {temp_c}°C")
#         # st.caption(f"Feels like {feels_like}°C")

#     c1, c2, c3, c4 = st.columns(4)
#     with c1: st.metric("Humidity", f"{humidity}%")
#     with c2: st.metric("Wind", f"{wind_kph} kph")
#     # with c3: st.metric("Feels Like", f"{feels_like}°C")
#     with c4: st.metric("Location", f"{city_name}")

#     st.markdown("---")

#     # === 5-DAY FORECAST ===
#     st.subheader("3-Day Forecast")

#     forecast_list = forecast_raw["forecast"]["forecastday"]
#     for day in forecast_list:
#         d = day["day"]
#         date_str = day["date"]
#         day_name = pd.to_datetime(date_str).strftime("%A")[:3]
#         icon = "https:" + d["condition"]["icon"] if d["condition"]["icon"].startswith("//") else d["condition"]["icon"]

#         cols = st.columns([1, 2, 3, 2])
#         with cols[0]:
#             st.image(icon, width=60)
#         with cols[1]:
#             st.markdown(f"**{day_name}**")
#             st.caption(date_str[5:])
#         with cols[2]:
#             st.markdown(f"**{d['maxtemp_c']}°** / {d['mintemp_c']}°")
#             st.caption(d["condition"]["text"])
#         with cols[3]:
#             rain = d["daily_chance_of_rain"]
#             st.progress(rain / 100)
#             st.caption(f"Rain: {rain}%")

#     st.markdown("---")

#     # # === TEMPERATURE CHART ===
#     # st.subheader("Temperature Trend ")

#     # chart_df = pd.DataFrame([
#     #     {
#     #         "Date": pd.to_datetime(day["date"]).strftime("%b %d"),
#     #         "Max °C": day["day"]["maxtemp_c"],
#     #         "Min °C": day["day"]["mintemp_c"],
#     #         "Avg °C": day["day"]["avgtemp_c"]
#     #     }
#     #     for day in forecast_list
#     # ])

#     # chart = alt.Chart(chart_df).transform_fold(
#     #     ["Max °C", "Min °C", "Avg °C"]
#     # ).mark_line(point=True).encode(
#     #     x="Date:T",
#     #     y="value:Q",
#     #     color="key:N",
#     #     tooltip=["Date", "key", "value"]
#     # ).properties(height=320)

#     # st.altair_chart(chart, use_container_width=True)

#         # === TEMPERATURE CHART (FIXED & BEAUTIFUL) ===
#     st.subheader("Temperature Trend ")

#     chart_data = []
#     for day in forecast_list:
#         date_fmt = pd.to_datetime(day["date"]).strftime("%b %d")
#         chart_data.extend([
#             {"Date": date_fmt, "Temperature (°C)": day["day"]["maxtemp_c"], "Type": "Max"},
#             {"Date": date_fmt, "Temperature (°C)": day["day"]["mintemp_c"], "Type": "Min"},
#             {"Date": date_fmt, "Temperature (°C)": day["day"]["avgtemp_c"], "Type": "Avg"}
#         ])

#     df_chart = pd.DataFrame(chart_data)

#     chart = alt.Chart(df_chart).mark_line(
#         point=alt.OverlayMarkDef(size=100)
#     ).encode(
#         x=alt.X("Date:N", title="Date", sort=None),
#         y=alt.Y("Temperature (°C):Q", scale=alt.Scale(zero=False)),
#         color=alt.Color("Type:N", legend=alt.Legend(title="Temperature")),
#         tooltip=["Date", "Type", "Temperature (°C)"]
#     ).properties(
#         height=340,
#         width="container"
#     ).configure_point(
#         size=120
#     ).configure_legend(
#         orient="top"
#     )

#     st.altair_chart(chart, use_container_width=True)

#     # Buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Refresh All Data"):
#             st.rerun()
#     with col2:
#         if st.button("New Search"):
#             for k in ["selected_city", "show_weather", "last_search"]:
#                 st.session_state[k] = "" if k != "show_weather" else False
#             st.rerun()

# else:
#     st.info("Start typing a city name above to see weather & forecast!")

# # === FOOTER ===
# st.markdown("---")
# st.caption("Vayu • Built with love using Streamlit • Powered by WeatherAPI")


import streamlit as st
import pandas as pd
import altair as alt
from utils.api import get_current_weather, get_forecast_weather, search_cities


# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Vayu Weather Dashboard",
    page_icon="☁️",
    layout="centered"
)

st.title("🌤️ Vayu – Weather Companion")
st.caption("Live Current Weather & 3-Day Forecast")


# ========== STATE MANAGEMENT ==========
for key in ["selected_city", "show_weather", "last_search"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "show_weather" else False


# ========== CITY SEARCH ==========
search_query = st.text_input(
    "Search a city:",
    placeholder="e.g., Mumbai, London, Tokyo"
)

if search_query != st.session_state.last_search:
    st.session_state.show_weather = False
    st.session_state.last_search = search_query

if search_query and len(search_query) >= 2:
    with st.spinner("Searching..."):
        results = search_cities(search_query)

    if results:
        selected = st.selectbox(
            "Select a result:",
            [""] + [r["name"] for r in results]
        )
        if selected:
            st.session_state.selected_city = selected
            st.session_state.show_weather = True
            st.success(f"City Selected: **{selected}**")
    else:
        st.warning("No matching cities found.")


# ========== WEATHER DISPLAY ==========
if st.session_state.show_weather and st.session_state.selected_city:

    city = st.session_state.selected_city

    with st.spinner("Fetching weather data..."):
        current = get_current_weather(city)
        forecast = get_forecast_weather(city)

    # ---- Error Handling ----
    if "error" in current:
        st.error(current["error"])
        st.stop()
    if "error" in forecast:
        st.error(forecast["error"])
        st.stop()

    # ---- Display Current Weather ----
    icon_url = "https:" + current["icon"] if current["icon"].startswith("//") else current["icon"]

    st.markdown(f"## 📍 {current['city']}, {current['region']}")
    st.markdown(f"### {current['condition']}")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(icon_url, width=120)
    with col2:
        st.markdown(f"### 🌡️ {current['temp_c']}°C")

    metrics = st.columns(4)
    metrics[0].metric("Humidity", f"{current['humidity']}%")
    metrics[1].metric("Wind", f"{current['wind_kph']} kph")

    # safe field usage
    feels_like = current.get("feels_like_c", "N/A")
    metrics[2].metric("Feels Like", f"{feels_like}°C")

    metrics[3].metric("Region", current["region"])

    st.markdown("---")

    # ---- Display Forecast ----
    st.subheader("📅 3-Day Forecast")
    days = forecast.get("forecast", [])

    for day in days:
        icon = "https:" + day["icon"] if day["icon"].startswith("//") else day["icon"]

        row = st.columns([1, 2, 3, 2])

        with row[0]:
            st.image(icon, width=60)

        with row[1]:
            st.markdown(f"**{day['day_name']}**")
            st.caption(day["date"])

        with row[2]:
            st.markdown(f"🌡️ {day['max_temp']}° / {day['min_temp']}°")
            st.caption(day["condition"])

        with row[3]:
            rain = day.get("chance_of_rain", 0)
            st.progress(rain / 100)
            st.caption(f"{rain}% Rain")

    st.markdown("---")

    # ---- Temperature Trend Graph ----
    st.subheader("📈 Temperature Trend")

    chart_df = pd.DataFrame([
        {"Date": d["date"], "Value": d["max_temp"], "Type": "Max"} for d in days
    ] + [
        {"Date": d["date"], "Value": d["min_temp"], "Type": "Min"} for d in days
    ])

    chart = alt.Chart(chart_df).mark_line(point=True).encode(
        x="Date:N",
        y="Value:Q",
        color="Type:N",
        tooltip=["Date", "Type", "Value"]
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)

    # ---- Buttons ----
    col1, col2 = st.columns(2)
    if col1.button("🔄 Refresh"):
        st.rerun()
    if col2.button("🆕 New Search"):
        st.session_state.selected_city = ""
        st.session_state.show_weather = False
        st.rerun()

else:
    st.info("Start typing a city above to get weather ☁️")


# ========== FOOTER ==========
st.markdown("---")
st.caption("🌦️ Built with Streamlit • Powered by WeatherAPI • Made with ❤️")

