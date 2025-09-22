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

def animate_circle(m, rad, latlon):
    circle = folium.Circle(
        location=latlon,
        radius=rad,
        color="red",
        fill=True,
        fill_color="lightblue"
    ).add_to(m)

    circle.add_child(AnimateCircle())