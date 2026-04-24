import streamlit as st
import streamlit_card
from cogs.weather_api import Weather
import streamlit_extras.dataframe_explorer as df_explorer

st.set_page_config(page_title='Weather Lens', layout='wide')
st.title('🌦️ Weather Lens | Forecast at a Glance')
st.subheader('In Development')

def load_weather():
    location : str = st.session_state.get('location')
    weather = Weather(location.replace(',', ' ').lower())
    st.session_state['weather_data'] = weather


weather : Weather = st.session_state.get('weather_data')

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

    
    left, right = st.columns(2)
    with left:
        streamlit_card.card(
            title  = f"{round(weather.current.get('temp_c'))}°C",
            text   = [
                f"{weather.location.get('name')}, {weather.location.get('region')}, {weather.location.get('country')}",
                f"{weather.current.get('last_updated')}"
            ],
            image  = weather.get_bg_image(),
            styles = {
                'card' : {
                    'height' : '400px',
                    'width' : '100%',
                },
                'title' : {
                    'font-size' : 60
                },
                'text' : {
                    'font-size' : 30
                }
            }
        )


    with right:
        st.subheader('Hourly Weather : ')
        df = df_explorer.dataframe_explorer(weather.hourly_df_generator(), case=False)
        st.dataframe(df, hide_index=True)  

    st.divider()