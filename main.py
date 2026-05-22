from graph import plot_all_cities
import requests
import pandas as pd
from datetime import datetime
import os

API_KEY = 'KEY_HERE'

cities = [
    'Rio de Janeiro',
    'São Paulo',
    'Belo Horizonte',
    'Porto Alegre'
]


os.makedirs('data', exist_ok=True)

while True:

    print('\n========== SKYDATA ==========')
    print('\nSelect an option:\n')

    for index, city in enumerate(cities, start=1):
        print(f'{index} - {city}')

    print('5 - Show graph')
    print('0 - Exit')

    option = input('\nEnter the option number: ')

    if option == '0':
        print('\nClosing SkyData...')
        break

    if not option.isdigit():
        print('\nInvalid option!')
        continue

    option = int(option)

    if option == 5:
        plot_all_cities()
        continue

    if option < 1 or option > len(cities):
        print('\nInvalid option!')
        continue

    city = cities[option - 1]

    url = (
        f'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city}&appid={API_KEY}&lang=en&units=metric'
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:

        now = datetime.now()

        weather_data = {
            'date': [now.strftime('%d/%m/%Y')],
            'time': [now.strftime('%H:%M:%S')],
            'city': [data['name']],
            'temperature': [data['main']['temp']],
            'feels_like': [data['main']['feels_like']],
            'humidity': [data['main']['humidity']],
            'weather': [data['weather'][0]['description']],
            'wind_speed': [data['wind']['speed']]
        }

        df = pd.DataFrame(weather_data)

        file_path = 'data/weather.csv'
        file_exists = os.path.isfile(file_path)

        try:

            df.to_csv(
                file_path,
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