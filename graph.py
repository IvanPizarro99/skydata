import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_all_cities():

    file_path = 'data/weather.csv'

    if not os.path.isfile(file_path):
        print('No data found!')
        return

    df = pd.read_csv(file_path, sep=';')

    if df.empty:
        print('CSV is empty!')
        return

    # Converte temperatura
    df['temperature'] = pd.to_numeric(df['temperature'])

    # Converte data
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    # Média por dia e cidade
    grouped = (
        df.groupby(['date', 'city'])['temperature']
        .mean()
        .reset_index()
    )

    # Tamanho do gráfico
    plt.figure(figsize=(12, 6))

    # Cria linha para cada cidade
    for city in grouped['city'].unique():

        city_data = grouped[grouped['city'] == city]

        plt.plot(
            city_data['date'],
            city_data['temperature'],
            marker='o',
            label=city
        )

    plt.title('Average Daily Temperature')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')

    plt.xticks(rotation=45)

    plt.grid(True, linestyle='--', alpha=0.5)

    plt.legend()

    plt.tight_layout()

    plt.show()