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
    location : str = st.session_state.get('location')
    x = Weather(location.replace(',', ' ').lower())
    x.get_response()
    st.session_state['weather_data'] = x

left, right = st.columns([2, 1])

with left :
    st.selectbox(
        label='',
        label_visibility='collapsed',
        placeholder = 'Enter a city, state or country',
        options     = get_base_locations(),
        on_change   = load_weather,
        key         = 'location',
        index       = None,
        accept_new_options = True
    )

with right:
    if obj:=st.session_state.get('weather_data'):
        if obj.response.get('error'):
            st.error('''Location not found please add state and/or country with it.
                    \nExample : 
                    \n\t- Bengalore Karnataka 
                    \n\t- Bengalore Karnataka India''')
        else:
            st.success(json.dumps(obj.location, indent=4))