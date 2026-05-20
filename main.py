from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
history = []
#---------------def weather()---------------------------
@app.get("/weather/{city}")
def get_weather(city: str):

    history.append(city)

    url = (
        f"https://api.weatherapi.com/v1/current.json"
        f"?key={API_KEY}&q={city}&aqi=no"
    )

    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return {
            "error": "city not found"
        }

    data = response.json()

    return {
        "city": city,
        "temperature": data["current"]["temp_c"],
        "feels_like": data["current"]["feelslike_c"],
        "condition": data["current"]["condition"]["text"],
        'chanceofrain': data["current"]["chance_of_rain"],
        'text': data["current"]["condition"]["text"],
        'icon': data["current"]["condition"]["icon"],
        'is_day':data["current"]["is_day"],
    }


#---------------def forecast()---------------------------
@app.get("/forecast/{city}")
def get_forecast(city: str):
    
    history.append(city + ' - forecast')

    url = (
        f"https://api.weatherapi.com/v1/forecast.json"
        f"?key={API_KEY}&q={city}&aqi=no"
    )

    response = requests.get(url)
    if response.status_code != 200:
        return {
            "error": "city not found"
        }

    data = response.json()

    hours = data['forecast']['forecastday'][0]['hour']
    forecast = []
    for hour in hours:
        forecast.append({
            'time' : hour['time'],
            'temperature' : hour['temp_c'],
            'feels': hour['feelslike_c'],
            'text': hour['condition']['text'],
            'icon': hour['condition']['icon'],
            'chance_of_rain': hour['chance_of_rain']
        })
    return forecast


#---------------def history()---------------------------
@app.get("/history")
def get_history():
    return {
        "history": history
    }