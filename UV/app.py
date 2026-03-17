 


import streamlit as st
import pandas as pd

from services.weather import get_weather, get_weather_icon
from services.location import get_location
from services.search import search_duckduckgo

st.set_page_config(
    page_title="Python Utility Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

/* Animated background */
.stApp {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #0f2027, #203a43);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

/* Animation */
@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

/* Premium cards */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(8px);
    text-align: center;
}

.search-card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

h1,h2,h3,h4,p,div,label{
color:white !important;
}

</style>
""", unsafe_allow_html=True)



# Animated background
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #0f2027, #203a43);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

h1, h2, h3, h4, p, label, div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔧 Utility Tools")
option = st.sidebar.radio(
    "Select Tool",
    ["🌤 Weather Reporter", "📍 Location Finder", "🔎 DuckDuckGo Search"]
)

st.title("🚀 Python Utility Dashboard")
st.write("A Professional Multi-Tool Web App built with Streamlit")

 
 

if option == "🌤 Weather Reporter":

    st.header("🌤 Weather Reporter")

    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):

        if not city.strip():
            st.warning("⚠ Please enter a valid city name.")
        else:
            with st.spinner("Fetching weather data..."):
                result = get_weather(city)

            if "error" in result:
                st.error(result["error"])
            else:

                icon = get_weather_icon(result["description"])

                st.markdown(f"## {icon} Weather in {city.title()}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="card">
                    <h4>🌡 Temperature</h4>
                    <h2>{result['temperature']} °C</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="card">
                    <h4>💧 Humidity</h4>
                    <h2>{result['humidity']} %</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="card">
                    <h4>🌬 Wind Speed</h4>
                    <h2>{result['wind_speed']} m/s</h2>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("---")

                st.subheader("📊 7 Day Temperature Comparison")

                df_temp = pd.DataFrame({
                    "Date": result["forecast_dates"],
                    "Min Temp": result["forecast_min"],
                    "Max Temp": result["forecast_max"]
                })

                st.bar_chart(df_temp.set_index("Date"))

                st.subheader("📉 Pressure Trend (Next Hours)")

                df_pressure = pd.DataFrame({
                    "Time": pd.to_datetime(result["pressure_times"]).strftime("%H:%M"),
                    "Pressure": result["pressure_values"]
                })

                st.line_chart(df_pressure.set_index("Time"))















# ------------------------------------------------------
# LOCATION SECTION
# ------------------------------------------------------
elif option == "📍 Location Finder":

    st.header("📍 Location Finder")
    place = st.text_input("Enter Place Name (City, Landmark, Address)")

    if st.button("Find Location"):

        if not place.strip():
            st.warning("⚠ Please enter a valid place name.")
        else:
            with st.spinner("Fetching location data..."):
                result = get_location(place)

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Location Report of {result['place']}")

                col1, col2 = st.columns(2)
                col1.write(f"🏠 Address: {result['address']}")
                col1.write(f"🌍 Latitude: {result['latitude']}")
                col1.write(f"🌍 Longitude: {result['longitude']}")

                maps_url = f"https://www.google.com/maps?q={result['latitude']},{result['longitude']}"
                col1.markdown(f"[🌐 Open in Google Maps]({maps_url})")

                map_data = pd.DataFrame({
                    "lat": [result["latitude"]],
                    "lon": [result["longitude"]]
                })
                col2.map(map_data)

                st.markdown("---")
                with st.expander("🔍 View Raw Location Data"):
                    st.json(result["raw_data"])

# ------------------------------------------------------
# SEARCH SECTION
# ------------------------------------------------------




elif option == "🔎 DuckDuckGo Search":

    st.header("🔎 DuckDuckGo Search")

    query = st.text_input("Enter Search Query")
    num_results = st.slider("Number of Results", 1, 10, 5)

    if st.button("Search"):

        with st.spinner("Searching DuckDuckGo..."):
            result = search_duckduckgo(query, num_results)

        if "error" in result:
            st.error(result["error"])

        else:

            st.success(f"Results for: {result['query']}")

            for item in result["text_results"]:

                st.markdown(f"""
                <div class="search-card">

                <h4>{item['title']}</h4>

                <a href="{item['url']}" target="_blank" style="color:#4cc9f0;">
                🔗 Visit Website
                </a>

                </div>
                """, unsafe_allow_html=True)