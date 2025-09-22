import folium
from streamlit_folium import st_folium
import streamlit as st
from branca.element import MacroElement
from jinja2 import Template


# Custom JavaScript for circle animation
class AnimateCircle(MacroElement):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var circle = {{this._parent.get_name()}};
        var r = circle.getRadius();
        function grow() {
            r += 500;
            if (r < 60000) {
                circle.setRadius(r);
                requestAnimationFrame(grow);
            }
        }
        grow();
        {% endmacro %}
    """)

def animate_circle(m, rad):
    circle = folium.Circle(
        location=st.session_state.displayed_latlon,
        radius=rad,
        color="red",
        fill=True,
        fill_color="lightblue"
    ).add_to(m)

    circle.add_child(AnimateCircle())

st.sidebar.title("Inputs")

# Create a session state for storing the latitude and longitude
if "latlon" not in st.session_state:
    st.session_state.latlon = [13, 122] # Get the value of the coordinates every clicked
if "displayed_latlon" not in st.session_state:
    st.session_state.displayed_latlon = [0, 0] # Get the value of last-clicked coordinate (Only executed when the simulate button was clicked)
if "show_circle" not in st.session_state:
    st.session_state.show_circle = False
if "circle_animating" not in st.session_state:
    st.session_state.circle_animating = False
if "curr_zoom" not in st.session_state:
    st.session_state.curr_zoom = 6
if "displayed_zoom" not in st.session_state:
    st.session_state.displayed_zoom = 6

sim_btn = st.sidebar.button("Simulate")
print(sim_btn)

if sim_btn:
    st.session_state.show_circle = True
    st.session_state.displayed_latlon = list(st.session_state.latlon)
    st.session_state.displayed_zoom = st.session_state.curr_zoom

# Create a Folium map
m = folium.Map(location=st.session_state.latlon, zoom_start=st.session_state.displayed_zoom)

# Enable click-for-marker
m.add_child(folium.LatLngPopup())

if st.session_state.show_circle:
    animate_circle(m, 30000)

# Show map in Streamlit and capture interaction
map_data = st_folium(m, width=700, height=500)

if map_data and map_data["last_clicked"]:
    st.session_state.latlon[0] = map_data["last_clicked"]["lat"]
    st.session_state.latlon[1] = map_data["last_clicked"]["lng"]

if map_data and "zoom" in map_data:
    st.session_state.curr_zoom = map_data["zoom"]