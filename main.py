import streamlit as st
import json
from cogs.weather_api import Weather

st.set_page_config(page_title='Weather Lens', layout='centered')
st.title('🌦️ Weather Lens | Forecast at a Glance')
st.subheader('In Development')


def get_base_locations():
    with open('base_locations.json', 'r') as f:
        return json.load(f)

def load_weather():
    location = st.session_state.get('location')
    x = Weather(location)
    x.get_response()
    st.session_state['weather_data'] = x

st.selectbox(
    label     = 'Enter a city, state or country',
    options   = get_base_locations(),
    on_change = load_weather,
    key       = 'location',
    index     = None
)


if obj:=st.session_state.get('weather_data'):
    st.write(json.dumps(obj.location, indent=4))