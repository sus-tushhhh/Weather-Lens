import streamlit as st
import streamlit_card
from cogs.weather_api import Weather
from datetime import datetime, timedelta

st.set_page_config(page_title='Weather Lens', layout='centered')
st.title('🌦️ Weather Lens | Forecast at a Glance')
st.subheader('In Development')

def load_weather():
    location : str = st.session_state.get('location')
    weather = Weather(location.replace(',', ' ').lower())
    st.session_state['weather_data'] = weather


weather : Weather = st.session_state.get('weather_data')


# left, right = st.columns([2, 1])

# with left :
location = st.selectbox(
    label='Select Location',
    label_visibility='collapsed',
    placeholder = 'Enter a city, state or country',
    options     = Weather.get_base_locations(),
    on_change   = load_weather,
    key         = 'location',
    index       = None,
    accept_new_options = True,
)

if weather:
    if not weather.get_response():
        st.error('''Location not found please add state and/or country with it.
                \nUse format : <city> <state> [country]
                \nExample : 
                \n\t- Bengalore Karnataka 
                \n\t- Bengalore Karnataka India''')
    else:
        st.success('Location successfully fetched.')

# with right:
if weather:
    streamlit_card.card(
        title  = f"{round(weather.current.get('temp_c'))}°C",
        text   = f"{weather.location.get('name')}, {weather.location.get('region')}, {weather.location.get('country')}",
        image  = weather.get_bg_image(),
        styles = {
            'card' : {
                'height' : '400px',
                'width' : '100%'
            },
            'title' : {
                'font-size' : 60
            },
            'text' : {
                'font-size' : 30
            }
        }
    )

st.divider()

if weather:
    st.subheader('Hourly Weather : ')

    hour = st.select_slider(
        label = 'Select Hour : ',
        options = [f'{i} : 00' for i in range(24)],
        label_visibility = 'collapsed',
        key = 'selected_hour'
    )

    if sh := st.session_state.get('selected_hour'):
        sh = int(sh[:2])
        sh_temp = weather.hourly[sh]
        hourly_weather_bg = weather.get_hourly_bg_images()

        streamlit_card.card(
            title  = f"{round(sh_temp.get('temp_c'))}°C",
            text   = f"{weather.location.get('name')}, {weather.location.get('region')}, {weather.location.get('country')}",
            image  = hourly_weather_bg[sh],
            styles = {
                'card' : {
                    'height' : '400px',
                    'width' : '100%'
                },
                'title' : {
                    'font-size' : 60
                },
                'text' : {
                    'font-size' : 30
                }
            }
        )

st.divider()