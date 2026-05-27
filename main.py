from pathlib import Path
import subprocess
import sys

APP_NAME = '416bbb07e207cf9aaaac3fc5eae8089e'

DATA_DIR = Path('data')
CSV_FILE = DATA_DIR / 'weather.csv'
DASHBOARD_FILE = Path('dashboard.py')

def check_files():
    DATA_DIR.mkdir(exist_ok=True)

    if not CSV_FILE.exists():
        print('\n[ERROR] weather.csv not found.\n')
        sys.exit()

    if not DASHBOARD_FILE.exists():
        print('\n[ERROR] dashboard.py not found.\n')
        sys.exit()

def start_dashboard():
    print(f'\nStarting {APP_NAME} Dashboard...\n')

    subprocess.run([
        'streamlit',
        'run',
        'dashboard.py'
    ])

def main():
    check_files()
    start_dashboard()

if __name__ == '__main__':
    main()