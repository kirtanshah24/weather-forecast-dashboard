import streamlit as st

# Page config must be first Streamlit command
st.set_page_config(
    page_title="Vayu - Weather Dashboard",
    page_icon="☁️",
    layout="centered"
)

# PORT : 8501

# App title
st.title("☁️ Vayu")
st.subheader("Real-time Weather Dashboard")

# Simple welcome
st.write("Welcome! Enter a city name to get started.")

# Test input
name = st.text_input("Enter your name :")
if name:
    st.success(f"Namaste, {name}! Let's check the weather soon.")
else:
    st.info("Type anything above to test!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Powered by WeatherAPI")