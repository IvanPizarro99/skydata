import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração
API_KEY = os.getenv('OPENWEATHER_API_KEY')
DATA_DIR = Path('data')
CSV_FILE = DATA_DIR / 'weather.csv'

# Cidades e estados do Brasil
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
    """Busca dados de clima da OpenWeather API"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{city_name},{state_code},BR",
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'pt_br'
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
        print(f"⚠️  Erro ao buscar dados de {city_name}: {str(e)}")
        return None

def main():
    """Coleta dados de todas as cidades e salva no CSV"""
    if not API_KEY:
        print("❌ OPENWEATHER_API_KEY não configurada no .env")
        return False
    
    print(f"🌍 Coletando dados de {len(CITIES)} cidades...")
    
    data_list = []
    
    for city_name, state_code in CITIES.items():
        print(f"📍 Buscando {city_name}...", end=' ')
        weather_data = get_weather_data(city_name, state_code)
        
        if weather_data:
            data_list.append(weather_data)
            print("✅")
        else:
            print("⚠️")
    
    if data_list:
        # Criar DataFrame
        df = pd.DataFrame(data_list)
        
        # Garantir que o diretório existe
        DATA_DIR.mkdir(exist_ok=True)
        
        # Salvar como CSV
        df.to_csv(CSV_FILE, sep=';', index=False, encoding='utf-8')
        
        print(f"\n✅ {len(data_list)} cidades atualizadas em {CSV_FILE}")
        return True
    else:
        print("\n❌ Nenhum dado foi coletado.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
