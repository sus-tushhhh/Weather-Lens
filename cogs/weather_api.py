import json
import httpx
import streamlit as st
from datetime import datetime

class Weather:
    def __init__(self, query:str):
        self.url = "http://api.weatherapi.com/v1/forecast.json"
        self.params = {
            'key' : st.secrets.weather_app.api_key,
            'dt'  : datetime.now().date(),
            'q'   : query 
        }
        
    def get_response(self):
        self.response : dict = httpx.get(url=self.url, params=self.params).json()
        
        if self.response.get('error'):
            print(self.response['error']['message'])
        else:
            print(self.response['location'])


if __name__ == '__main__':
    x = Weather('Delhi')
    x.get_response()