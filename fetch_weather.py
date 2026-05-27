"""Módulo para coleta de dados climáticos da OpenWeather API"""

import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv
from config import CITIES, CSV_FILE, DATA_DIR
from logger_config import get_logger

load_dotenv()
logger = get_logger('fetch_weather')
API_KEY = os.getenv('OPENWEATHER_API_KEY')

def validate_api_key():
    """Valida se a API key está configurada"""
    if not API_KEY:
        logger.error("OPENWEATHER_API_KEY não configurada no .env")
        return False
    logger.info("API key validada com sucesso")
    return True

def get_weather_data(city_name, state_code):
    """Busca dados de clima da OpenWeather API"""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
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
        
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout ao buscar dados de {city_name}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.warning(f"Erro HTTP para {city_name}: {str(e)}")
        return None
    except (requests.exceptions.RequestException, KeyError) as e:
        logger.warning(f"Erro ao buscar dados de {city_name}: {str(e)}")
        return None

def main():
    """Coleta dados de todas as cidades e salva no CSV"""
    if not validate_api_key():
        return False
    
    logger.info(f"🌍 Iniciando coleta de dados de {len(CITIES)} cidades...")
    
    data_list = []
    for city_name, state_code in CITIES.items():
        logger.info(f"📍 Buscando {city_name}...")
        weather_data = get_weather_data(city_name, state_code)
        if weather_data:
            data_list.append(weather_data)
        
    if data_list:
        df = pd.DataFrame(data_list)
        Path(DATA_DIR).mkdir(exist_ok=True)
        df.to_csv(CSV_FILE, sep=';', index=False, encoding='utf-8')
        logger.info(f"✅ {len(data_list)}/{len(CITIES)} cidades atualizadas em {CSV_FILE}")
        return True
    else:
        logger.error("❌ Nenhum dado foi coletado.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
