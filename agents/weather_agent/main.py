from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Always load the .env file next to this script
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError('OPENAI_API_KEY not found. Check agents/weather_agent/.env')

client = OpenAI(api_key=api_key)

def get_weather(city : str):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        return f"Weather in {response.text.strip()}"
    else:
        return f"Could not retrieve weather data for {city}."

def main():
    user_query = input('-> ')
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'user', 'content': user_query}
        ],
    )
    print(f"->> {response.choices[0].message.content}")


print(get_weather("Banagalore"))
