import requests
import pandas as pd
from datetime import datetime
import os

# OpenWeather API
API_KEY = '416bbb07e207cf9aaaac3fc5eae8089e'

cities = [
    'Rio de Janeiro',
    'São Paulo',
    'Belo Horizonte',
    'Porto Alegre'
]

while True:


    print('\nSelect the city:\n')

    for index, city in enumerate(cities, start=1):
        print(f'{index} - {city}')

    print('0 - Exit')

    option = input('\nEnter the option number: ')

    if option == '0':
        print('\nClosing SkyData...')
        break

    if not option.isdigit():
        print('\nInvalid option!')
        continue

    option = int(option)

    if option < 1 or option > len(cities):
        print('\nInvalid option!')
        continue

    city = cities[option - 1]

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=en&units=metric'

    response = requests.get(url)

    data = response.json()

    if response.status_code == 200:

        now = datetime.now()

        current_date = now.strftime('%d/%m/%Y')
        current_time = now.strftime('%H:%M:%S')

        weather_data = {
            'date': [current_date],
            'time': [current_time],
            'city': [data['name']],
            'temperature': [data['main']['temp']],
            'feels_like': [data['main']['feels_like']],
            'humidity': [data['main']['humidity']],
            'weather': [data['weather'][0]['description']],
            'wind_speed': [data['wind']['speed']]
        }

        df = pd.DataFrame(weather_data)

        file_exists = os.path.isfile('weather.csv')

        try:

            df.to_csv(
                'weather.csv',
                sep=';',
                index=False,
                mode='a',
                header=not file_exists,
                encoding='utf-8-sig'
            )

            print('\nData saved successfully!')

        except PermissionError:
            print('\nClose weather.csv before running the system!')

    else:
        print('\nAPI error')
        print(data)