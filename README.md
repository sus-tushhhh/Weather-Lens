Weather Lens

Weather Lens is a Streamlit-based weather forecasting web app that provides clean visual insights for yesterday, today, and tomorrow, along with interactive charts.

Features

- Weather data for:
    - Yesterday
    - Today
    - Tomorrow

- Visual charts for:
    - Temperature trends
    - Humidity
    - Wind speed
    - Rain probability

- Clean dark-themed UI built with Streamlit
- Secure API key handling using Streamlit Secrets
- Fast and lightweight interface

Tech Stack

- Frontend & Backend: Streamlit
- Language: Python
- Libraries:
    - Pandas
    - Matplotlib
    - Requests

API Key Setup (Important)

This project uses Streamlit Secrets to securely store the API key.

Step 1: Create secrets file

.streamlit/secrets.toml

Step 2: Add your API key

API_KEY = "your_api_key_here"

Installation & Running

Clone the repository

git clone https://github.com/sus-tushhhh/Weather-Lens.git
cd Weather-Lens

Install dependencies

pip install -r requirements.txt

Run the app

streamlit run app.py

How It Works

- Fetches weather data from an external API
- Processes data for yesterday, today, and tomorrow
- Displays structured information using Streamlit
- Visualizes trends using charts for better understanding

Project Structure

Weather-Lens/
│── assets/ # Icons and images
│── app.py # Main Streamlit app
│── requirements.txt # Dependencies
│── .streamlit/
│ └── secrets.toml # API key (not pushed to GitHub)

Future Improvements

- Auto location detection
- Better mobile responsiveness
- More advanced analytics
- Multi-city comparison

Contributing

Feel free to fork and improve the project.

License

MIT License

Author

Tushant
GitHub: https://github.com/sus-tushhhh
