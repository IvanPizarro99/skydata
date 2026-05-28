import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
DATA_DIR = Path('data')
CSV_FILE = DATA_DIR / 'weather.csv'

# Cities and states of Brazil
CITIES = {
    'Rio Branco': 'AC',
    'Maceió': 'AL',
    'Macapá': 'AP',
    'Manaus': 'AM',
    'Salvador': 'BA',
    'Fortaleza': 'CE',
    'Brasília': 'DF',
    'Vitória': 'ES',
    'Goiânia': 'GO',
    'São Luís': 'MA',
    'Cuiabá': 'MT',
    'Campo Grande': 'MS',
    'Belo Horizonte': 'MG',
    'Belém': 'PA',
    'João Pessoa': 'PB',
    'Curitiba': 'PR',
    'Recife': 'PE',
    'Teresina': 'PI',
    'Rio de Janeiro': 'RJ',
    'Natal': 'RN',
    'Porto Alegre': 'RS',
    'Porto Velho': 'RO',
    'Boa Vista': 'RR',
    'Joinville': 'SC',
    'São Paulo': 'SP',
    'Aracaju': 'SE',
    'Palmas': 'TO',
}

def get_weather_data(city_name, state_code):
    """Fetches weather data from the OpenWeather API"""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{city_name},{state_code},BR",
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'en'
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            'date': datetime.now().strftime('%d/%m/%Y'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'city': city_name,
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['main'].lower(),
            'wind_speed': round(data['wind']['speed'], 1)
        }
    except requests.exceptions.RequestException as e:
        print(f"[WARNING] Error fetching data for {city_name}: {str(e)}")
        return None

def main():
    """Collects weather data for all cities and appends it to the CSV file"""
    if not API_KEY:
        print("[ERROR] OPENWEATHER_API_KEY not configured in .env")
        return False
    
    print(f"Collecting weather data for {len(CITIES)} cities...")
    
    data_list = []
    
    for city_name, state_code in CITIES.items():
        print(f"Fetching {city_name}...", end=' ')
        weather_data = get_weather_data(city_name, state_code)
        
        if weather_data:
            data_list.append(weather_data)
            print("OK")
        else:
            print("FAILED")
    
    if data_list:
        df = pd.DataFrame(data_list)
        
        DATA_DIR.mkdir(exist_ok=True)
        
        # Check if the file already exists to decide if we need a header row
        file_exists = CSV_FILE.exists()
        
        # Save by appending to the file instead of overwriting it
        df.to_csv(
            CSV_FILE, 
            sep=';', 
            index=False, 
            mode='a', 
            header=not file_exists, 
            encoding='utf-8'
        )
        
        print(f"\n[SUCCESS] {len(data_list)} cities updated in {CSV_FILE}")
        return True
    else:
        print("\n[ERROR] No data was collected.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)