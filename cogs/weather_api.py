import json
import httpx
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import base64

class Weather:
    def __init__(self, query:str, date:datetime = datetime.now().date(), day:str = 'today'):
        self.day    = day
        self.url    = "http://api.weatherapi.com/v1/forecast.json"
        self.query  = query
        self.params = {
            'key' : st.secrets.weather_app.api_key,
            'dt'  : date,
            'q'   : query 
        }
        

    def get_response(self):
        try:
            self.response : dict = httpx.get(url=self.url, params=self.params, timeout=10).json()
        
            if self.response.get('error'):
                return False
            else:
                self.location    : dict = self.response.get('location')
                self.current     : dict = self.response.get('current')
                self.forecast    : dict = self.response.get('forecast')
                self.forecastday : dict = self.forecast.get('forecastday')[0]
                self.today       : dict = self.forecastday.get('day')
                self.astro       : dict = self.forecastday.get('astro')
                self.hourly      : list[dict] = self.forecastday.get('hour')
                if self.day == 'today':
                    self.tomorrow   : Weather = Weather(self.query, (datetime.now() + timedelta(days=1)).date(), day='tomorrow')
                    self.tomorrow.get_response()
                return True
                
        except httpx.ConnectTimeout as e:
            return False

        except Exception as e:
            return False


    @staticmethod
    def get_base_locations():
        with open('assets/base_locations.json', 'r') as f:
            return json.load(f)


    def __get_path_of_bg(self, fp: str):
        with open(fp, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data)
            return  "data:image/png;base64," + encoded.decode("utf-8")


    def get_bg_image(self, hour: dict = None):
        if not hour:
            hour = self.current

        text = hour.get('condition').get('text').lower()

        if any([i in text for i in ['rain', 'drizzle']]):
            fp = r'assets/rain.png'
        elif any([i in text for i in ['sunny', 'clear']]):
            if hour.get('is_day'):
                fp = r'assets/dayclear.png'
            else :
                fp = r'assets/nightclear.png'
        elif any([i in text for i in ['cloudy', 'overcast']]):
            fp = r'assets/cloudy.png'
        elif any([i in text for i in ['mist', 'fog']]):
            fp = r'assets/fog.png'
        elif 'thunder' in text:
            fp = r'assets/thunder.png'
        elif 'snow' in text:
            if hour.get('is_day'):
                fp = r'assets/daysnowy.png'
            else :
                fp = r'assets/nightsnowy.png'
        else:
            return None
        
        return self.__get_path_of_bg(fp)
        

    def get_hourly_bg_images(self):
        l = []
        for i in self.hourly:
            l.append(self.get_bg_image(i))
        return l
    

    def hourly_df_generator(self):
        df = pd.DataFrame(self.hourly, columns=['time', 'temp_c', "feelslike_c", 'humidity'])
        df['time'] = df['time'].str[-5:-3].astype(int)
        df.columns = ['Hour', 'Today', 'Feels Like', 'Humidity']
        
        if self.day == 'today':
            tomorrow_df = (self.tomorrow.hourly_df_generator()).rename(columns={'Today' : 'Tomorrow'})
            df = df.merge(tomorrow_df.loc[:, ['Hour', 'Tomorrow']], on='Hour') 
        return df



if __name__ == '__main__':
    x = Weather("Delhi")
    x.get_response()
    print(x.current.get('condition').get('text'))
    print(x.get_bg_image())