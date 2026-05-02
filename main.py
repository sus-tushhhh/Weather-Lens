import streamlit as st
import streamlit_card
from cogs.weather_api import Weather
from streamlit_extras.chart_container import chart_container as stx_chart_container
from streamlit_extras.grid import grid as stx_grid
from PIL import Image

st.set_page_config(page_title='Weather Lens', layout='wide')
st.title('🌦️ Weather Lens | Forecast at a Glance')
st.subheader('In Development')

def load_weather():
    location : str = st.session_state.get('location')
    if location == 'Detect Location':
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
                            'font-size' : 30
                        }
                    }
                )


        with right:
           with st.container(border=True, height=450, vertical_alignment='center'):
                with stx_chart_container(weather.hourly_df_generator()):
                    st.line_chart(weather.hourly_df_generator().loc[:, ['Today', 'Tomorrow']],
                                x_label = 'Time (in 24-hour format)',
                                y_label = 'Temperature (°C)',
                                color   = ['Blue', 'Red'],
                    )
        
        st.divider()

        with st.container():
            grid = stx_grid(2, 3, 2, vertical_align='center')

            logos = [
                [r'assets/logos/min_temp.png',r'assets/logos/max_temp.png'],
                [r'assets/logos/humidity.png', r'assets/logos/wind_speed.png', r'assets/logos/chances_of_rain.png'],
                [r'assets/logos/sunrise.png', r'assets/logos/sunset.png']
            ]
            today = weather.today
            texts = [
                [f'Min : {today.get("mintemp_c")}°C', f'Max : {today.get("maxtemp_c")}°C'],
                [f'Humidity : {weather.current.get("humidity")}%', f'Wind : {weather.current.get("wind_kph")} km/ph', f'Rain Chances : {today.get("daily_chance_of_rain")}%'],
                [f'Sunrise : {weather.astro.get("sunrise")}', f'Sunset : {weather.astro.get("sunset")}']
            ]

            for l_row, t_row in zip(logos, texts) :
                for l_item, t_item in zip(l_row, t_row):
                    with grid.container(border=True):
                        logo, text = st.columns([1, 7], vertical_alignment='center')
                        with logo:
                            logo = Image.open(l_item).resize((75, 75))
                            st.image(logo)
                        with text:
                            st.header(t_item)

    else:
        st.error('''Location not found please add state and/or country with it.
                \nUse format : <city> <state> [country]
                \nExample : 
                \n\t- Bengalore Karnataka 
                \n\t- Bengalore Karnataka India''')
    


