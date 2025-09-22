import folium
from streamlit_folium import st_folium
import streamlit as st
from branca.element import MacroElement
from jinja2 import Template

# Custom JavaScript for circle animation
class AnimateCircle(MacroElement):
    def __init__(self, max_radius):
        super().__init__()
        self._name = "AnimateCircle"
        self.max_radius = max_radius

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            var circle = {{this._parent.get_name()}};
            var r = circle.getRadius();
            var maxR = {{this.max_radius}};
            function grow() {
                r += 100;
                if (r < maxR) {
                    circle.setRadius(r);
                    requestAnimationFrame(grow);
                }
            }
            grow();
            {% endmacro %}
        """)

    def render(self, **kwargs):
        # inject max_radius into template context
        self._template.module.max_radius = int(self.max_radius)
        super().render(**kwargs)


def animate_circle(m, rad, latlon, clr):
    circle = folium.Circle(
        location=latlon,
        radius=0,  # start at 0, will grow
        color=clr,
        fill=True,
        fill_color="lightblue"
    ).add_to(m)

    circle.add_child(AnimateCircle(rad))
