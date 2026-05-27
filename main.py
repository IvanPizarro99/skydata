import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Getting API key from environment
API_KEY = os.getenv('key')

print("Opening SkyData dashboard...")

os.system("streamlit run dashboard.py")