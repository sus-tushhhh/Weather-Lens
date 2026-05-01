import streamlit as st
import streamlit_card
from cogs.weather_api import Weather
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container

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
    if weather.get_response():
        st.success('Location successfully fetched.')


        left, right = st.columns(2)
        with left:
            with st.container(border=True, height=450, vertical_alignment='center'):
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
                            'margin' : '0px',
                            'transform' : 'none !important',
                            'transition' : 'none !important'
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
           with st.container(border=True, height=450, vertical_alignment='center'):
                with chart_container(weather.hourly_df_generator()):
                    st.line_chart(weather.hourly_df_generator().loc[:, ['Today', 'Tomorrow']],
                                x_label = 'Time (in 24-hour format)',
                                y_label = 'Temperature (°C)'
                    )
        
        st.divider()

    else:
        st.error('''Location not found please add state and/or country with it.
                \nUse format : <city> <state> [country]
                \nExample : 
                \n\t- Bengalore Karnataka 
                \n\t- Bengalore Karnataka India''')
    


