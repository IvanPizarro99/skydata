from pathlib import Path
import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = '416bbb07e207cf9aaaac3fc5eae8089e'

DATA_DIR = Path('data')
CSV_FILE = DATA_DIR / 'weather.csv'
DASHBOARD_FILE = Path('dashboard.py')
FETCH_FILE = Path('fetch_weather.py')

def check_files():
    DATA_DIR.mkdir(exist_ok=True)

    if not DASHBOARD_FILE.exists():
        print('\n[ERROR] dashboard.py not found.\n')
        sys.exit()
    
    if not FETCH_FILE.exists():
        print('\n[ERROR] fetch_weather.py not found.\n')
        sys.exit()

def fetch_weather():
    """Executa o script de coleta de dados da API"""
    print('\n📡 Atualizando dados climáticos da API...\n')
    
    try:
        subprocess.run([
            sys.executable,
            'fetch_weather.py'
        ], check=True)
        print('\n✅ Dados climáticos atualizados!\n')
    except subprocess.CalledProcessError:
        print('\n⚠️  Falha ao atualizar dados da API. Continuando com dados existentes...\n')
    except Exception as e:
        print(f'\n⚠️  Erro ao executar fetch_weather.py: {str(e)}\n')

def start_dashboard():
    print(f'\nStarting {APP_NAME} Dashboard...\n')

    subprocess.run([
        'streamlit',
        'run',
        'dashboard.py'
    ])

def main():
    check_files()
    fetch_weather()
    start_dashboard()

if __name__ == '__main__':
    main()
