from pathlib import Path
import subprocess
import sys
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
        print(f'\n[ERROR] {DASHBOARD_FILE.name} not found.\n')
        sys.exit(1)
    
    if not FETCH_FILE.exists():
        print(f'\n[ERROR] {FETCH_FILE.name} not found.\n')
        sys.exit(1)

def fetch_weather():
    """Executes the API data collection script"""
    print('\nUpdating weather data from the API...\n')
    
    try:
        subprocess.run([
            sys.executable,
            str(FETCH_FILE)
        ], check=True)
        print('\nWeather data updated successfully!\n')
    except subprocess.CalledProcessError:
        print('\nFailed to update API data. Continuing with existing data...\n')
    except Exception as e:
        print(f'\nError executing {FETCH_FILE.name}: {str(e)}\n')

def start_dashboard():
    print(f'\nStarting {APP_NAME} Dashboard...\n')

    try:
        subprocess.run([
            'streamlit',
            'run',
            str(DASHBOARD_FILE)
        ], check=True)
    except KeyboardInterrupt:
        print('\nDashboard server stopped by user.\n')
    except Exception as e:
        print(f'\nError starting dashboard: {str(e)}\n')

def main():
    check_files()
    fetch_weather()
    start_dashboard()

if __name__ == '__main__':
    main()