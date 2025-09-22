import folium
from streamlit_folium import st_folium
import streamlit as st
from animation.circle_animation import animate_circle
from impactor import Impactor
import math

### Session States
if "latlon" not in st.session_state:
    st.session_state.latlon = [13, 122] # Get the value of the coordinates every clicked
if "displayed_latlon" not in st.session_state:
    st.session_state.displayed_latlon = [0, 0] # Get the value of last-clicked coordinate (Only executed when the simulate button was clicked)
if "show_circle" not in st.session_state:
    st.session_state.show_circle = False
if "curr_zoom" not in st.session_state:
    st.session_state.curr_zoom = 6
if "displayed_zoom" not in st.session_state:
    st.session_state.displayed_zoom = 6
if "impactor" not in st.session_state:
    st.session_state.impactor = Impactor(50.0, 20000.0, "Iron", 90)

#### UI
st.sidebar.title("Inputs")
with st.sidebar.form(key="input_parameters"):
    st.session_state.impactor.radius = st.number_input("Asteroid radius (m)", min_value=1.0, value=st.session_state.impactor.radius, step=1.0)
    st.session_state.impactor.velocity = st.number_input("Velocity (m/s)", min_value=1000.0, value=st.session_state.impactor.velocity, step=1000.0)
    st.session_state.impactor.angle = st.slider("Impact angle (degrees)", 0, 90, int(st.session_state.impactor.angle))
    st.session_state.impactor.composition = st.selectbox("Impactor composition", ["Stony", "Iron", "Carbonaceous", "Comet"])
    target = st.selectbox("Target type", ["Rock", "Water", "Sedimentary_Rock"])
    sim_btn = st.form_submit_button("Simulate")

#### On Simulation Button Click
if sim_btn:
    st.session_state.show_circle = True
    st.session_state.displayed_latlon = list(st.session_state.latlon)
    st.session_state.displayed_zoom = st.session_state.curr_zoom
    # st.session_state.impactor = Impactor(radius, velocity, composition, angle)

tab1, tab2, tab3 = st.tabs(["Crater", "Thermal Exposure", "Shockwave"])

with tab1:
    st.header("Crater")
    # Create a Folium map
    map1 = folium.Map(location=st.session_state.displayed_latlon, zoom_start=st.session_state.displayed_zoom, key="map1")
    map1.add_child(folium.LatLngPopup()) # Enable click-for-marker

    # Draw and Animate Circle
    if st.session_state.show_circle:
        animate_circle(map1, st.session_state.impactor.transient_crater_diameter(), st.session_state.displayed_latlon, "red")
        # animate_circle(m, st.session_state.impactor.transient_crater_diameter()+10000, st.session_state.displayed_latlon)

    # Show map in Streamlit and capture interaction
    map1_data = st_folium(map1, width=700, height=500)

    # # Capture latitude and longitude every clicked
    if map1_data and map1_data["last_clicked"]:
        st.session_state.latlon[0] = map1_data["last_clicked"]["lat"]
        st.session_state.latlon[1] = map1_data["last_clicked"]["lng"]

    # # Capture zoom data every zoom
    if map1_data and "zoom" in map1_data:
        st.session_state.curr_zoom = map1_data["zoom"]
    
with tab2:
    st.header("Thermal Exposure")
    # Create a Folium map
    map2 = folium.Map(location=st.session_state.displayed_latlon, zoom_start=st.session_state.displayed_zoom, key="map2")
    map2.add_child(folium.LatLngPopup()) # Enable click-for-marker

    # Draw and Animate Circle
    if st.session_state.show_circle:
        animate_circle(map2, st.session_state.impactor.fireball_radius(), st.session_state.displayed_latlon, "orange")
        print(st.session_state.impactor.fireball_radius())
        # animate_circle(m, st.session_state.impactor.transient_crater_diameter()+10000, st.session_state.displayed_latlon)

    # Show map in Streamlit and capture interaction
    map2_data = st_folium(map2, width=700, height=500)

    # Capture latitude and longitude every clicked
    if map2_data and map2_data["last_clicked"]:
        st.session_state.latlon[0] = map2_data["last_clicked"]["lat"]
        st.session_state.latlon[1] = map2_data["last_clicked"]["lng"]

    # Capture zoom data every zoom
    if map2_data and "zoom" in map2_data:
        st.session_state.curr_zoom = map2_data["zoom"]

with tab3:
    st.header("Shock Wave")
    # Create a Folium map
    map3 = folium.Map(location=st.session_state.displayed_latlon, zoom_start=st.session_state.displayed_zoom, key="map3")
    map3.add_child(folium.LatLngPopup()) # Enable click-for-marker

    # Draw and Animate Circle
    if st.session_state.show_circle:
        animate_circle(map3, st.session_state.impactor.transient_crater_diameter(), st.session_state.displayed_latlon, "white")
        # animate_circle(m, st.session_state.impactor.transient_crater_diameter()+10000, st.session_state.displayed_latlon)

    # Show map in Streamlit and capture interaction
    map3_data = st_folium(map3, width=700, height=500)

    # Capture latitude and longitude every clicked
    if map3_data and map3_data["last_clicked"]:
        st.session_state.latlon[0] = map3_data["last_clicked"]["lat"]
        st.session_state.latlon[1] = map3_data["last_clicked"]["lng"]

    # Capture zoom data every zoom
    if map3_data and "zoom" in map3_data:
        st.session_state.curr_zoom = map3_data["zoom"]