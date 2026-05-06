import streamlit as st
import streamlit_card
from cogs.weather_api import Weather
from streamlit_extras.chart_container import chart_container as stx_chart_container
from streamlit_extras.grid import grid as stx_grid
from streamlit_extras.metric_cards import *
from PIL import Image

st.set_page_config(page_title='Weather Lens', layout='wide')
st.title('🌦️ Weather Lens | Forecast at a Glance')

def load_weather():
    location : str = st.session_state.get('location')
    if location in 'Detect Location':
        weather = Weather('auto:ip')
    else:
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
                            'height' : '410px',
                            'width' : '100%',
                            'margin' : '0px',
                            'transform' : 'none !important',
                            'transition' : 'none !important'
                        },
                        'title' : {
                            'font-size' : 60
                        },
                        'text' : {
                            'font-size' : 30,
                            'color'     : '#9c9d9f'
                        }
                    }
                )


        with right:
           with st.container(border=True, height=450, vertical_alignment='center'):
                with stx_chart_container(weather.hourly_df_generator()):
                    st.line_chart(weather.hourly_df_generator().loc[:, ['Yesterday', 'Today', 'Tomorrow']],
                                x_label = 'Time (in 24-hour format)',
                                y_label = 'Temperature (°C)',
                                color   = ['#7C3AED', '#EC4899', '#FACC15'],
                    )


        sections = [
            (
                "Forecast :",
                [
                    [r'assets/logos/min_temp.png', r'assets/logos/max_temp.png'],
                    [r'assets/logos/humidity.png', r'assets/logos/chances_of_rain.png'],
                    [r'assets/logos/wind_speed.png']
                ],
                Weather.get_forecast_text
            ),
            (
                "Astrology :",
                [
                    [r'assets/logos/sunrise.png', r'assets/logos/sunset.png']
                ],
                Weather.get_astro_text
            )
        ]

        days = [
            ("Yesterday", weather.yesterday),
            ("Today", weather),
            ("Tomorrow", weather.tomorrow)
        ]

        for title, logos, data_func in sections:
            st.title(title)

            cols = st.columns(3, border=True)

            for col, (subtitle, data) in zip(cols, days):
                with col:
                    st.subheader(f"{subtitle} :")
                    grid = stx_grid(2, 2, 2, 2, vertical_align='center')

                    for l_row, t_row in zip(logos, data_func(data)):
                        for l_item, t_item in zip(l_row, t_row):
                            with grid.container(border=True):
                                c1, c2 = st.columns([1, 2], vertical_alignment='center')
                                c1.image(Image.open(l_item), width=75)
                                c2.metric(
                                    label=f"**:gray[{t_item[0]}]**",
                                    value=f"{t_item[1]}"
                                )
            

    else:
        st.error('''Location not found please add state and/or country with it.
                \nUse format : <city> <state> [country]
                \nExample : 
                \n\t- Bengalore Karnataka 
                \n\t- Bengalore Karnataka India''')
    


