import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from pathlib import Path
import geocoder

st.set_page_config(
    page_title='SkyData Dashboard',
    page_icon='🌦️',
    layout='wide'
)

city_to_state = {
    # Acre
    'Rio Branco': 'Acre',
    'Cruzeiro do Sul': 'Acre',
    
    # Alagoas
    'Maceió': 'Alagoas',
    'Rio Largo': 'Alagoas',
    
    # Amapá
    'Macapá': 'Amapá',
    'Santana': 'Amapá',
    
    # Amazonas
    'Manaus': 'Amazonas',
    'Parintins': 'Amazonas',
    
    # Bahia
    'Salvador': 'Bahia',
    'Feira de Santana': 'Bahia',
    'Vitória da Conquista': 'Bahia',
    'Ilhéus': 'Bahia',
    'Jequié': 'Bahia',
    
    # Ceará
    'Fortaleza': 'Ceará',
    'Caucaia': 'Ceará',
    'Juazeiro do Norte': 'Ceará',
    'Sobral': 'Ceará',
    
    # Distrito Federal
    'Brasília': 'Distrito Federal',
    
    # Espírito Santo
    'Vitória': 'Espírito Santo',
    'Vila Velha': 'Espírito Santo',
    'Serra': 'Espírito Santo',
    
    # Goiás
    'Goiânia': 'Goiás',
    'Aparecida de Goiânia': 'Goiás',
    'Anápolis': 'Goiás',
    
    # Maranhão
    'São Luís': 'Maranhão',
    'Imperatriz': 'Maranhão',
    'Caxias': 'Maranhão',
    
    # Mato Grosso
    'Cuiabá': 'Mato Grosso',
    'Várzea Grande': 'Mato Grosso',
    'Rondonópolis': 'Mato Grosso',
    
    # Mato Grosso do Sul
    'Campo Grande': 'Mato Grosso do Sul',
    'Dourados': 'Mato Grosso do Sul',
    'Três Lagoas': 'Mato Grosso do Sul',
    
    # Minas Gerais
    'Belo Horizonte': 'Minas Gerais',
    'Uberlândia': 'Minas Gerais',
    'Contagem': 'Minas Gerais',
    'Juiz de Fora': 'Minas Gerais',
    'Divinópolis': 'Minas Gerais',
    
    # Pará
    'Belém': 'Pará',
    'Ananindeua': 'Pará',
    'Marabá': 'Pará',
    'Santarém': 'Pará',
    
    # Paraíba
    'João Pessoa': 'Paraíba',
    'Campina Grande': 'Paraíba',
    'Patos': 'Paraíba',
    
    # Paraná
    'Curitiba': 'Paraná',
    'Londrina': 'Paraná',
    'Maringá': 'Paraná',
    'Ponta Grossa': 'Paraná',
    
    # Pernambuco
    'Recife': 'Pernambuco',
    'Jaboatão dos Guararapes': 'Pernambuco',
    'Olinda': 'Pernambuco',
    'Caruaru': 'Pernambuco',
    
    # Piauí
    'Teresina': 'Piauí',
    'Parnaíba': 'Piauí',
    'Picos': 'Piauí',
    
    # Rio de Janeiro
    'Rio de Janeiro': 'Rio de Janeiro',
    'Niterói': 'Rio de Janeiro',
    'Duque de Caxias': 'Rio de Janeiro',
    'São Gonçalo': 'Rio de Janeiro',
    
    # Rio Grande do Norte
    'Natal': 'Rio Grande do Norte',
    'Mossoró': 'Rio Grande do Norte',
    'Parnamirim': 'Rio Grande do Norte',
    
    # Rio Grande do Sul
    'Porto Alegre': 'Rio Grande do Sul',
    'Caxias do Sul': 'Rio Grande do Sul',
    'Pelotas': 'Rio Grande do Sul',
    'Santa Maria': 'Rio Grande do Sul',
    
    # Rondônia
    'Porto Velho': 'Rondônia',
    'Ariquemes': 'Rondônia',
    'Ji-Paraná': 'Rondônia',
    
    # Roraima
    'Boa Vista': 'Roraima',
    'Rorainópolis': 'Roraima',
    
    # Santa Catarina
    'Joinville': 'Santa Catarina',
    'Blumenau': 'Santa Catarina',
    'Florianópolis': 'Santa Catarina',
    'Chapecó': 'Santa Catarina',
    
    # São Paulo
    'São Paulo': 'São Paulo',
    'Guarulhos': 'São Paulo',
    'Campinas': 'São Paulo',
    'São Bernardo do Campo': 'São Paulo',
    'Santo André': 'São Paulo',
    
    # Sergipe
    'Aracaju': 'Sergipe',
    'Nossa Senhora do Socorro': 'Sergipe',
    
    # Tocantins
    'Palmas': 'Tocantins',
<<<<<<< HEAD
    'Araguaína': 'Tocantins',
=======
    'Araguaína': 'Tocantins'
>>>>>>> d36a605 (new version)
}

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #020617, #0f172a);
}

.block-container {
    padding-top: 2rem;
}

.title {
    text-align: center;
    color: white;
    font-size: 60px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 35px;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(10px);
    transition: 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    border: 1px solid #38bdf8;
    box-shadow: 0px 0px 25px rgba(56,189,248,0.4);
}

</style>
""", unsafe_allow_html=True)

csv_path = Path('data/weather.csv')
geojson_path = Path('data/brazil_states.geojson')

if not csv_path.exists():
    st.error('weather.csv not found.')
    st.stop()

if not geojson_path.exists():
    st.warning('brazil_states.geojson not found. Install it or provide the file.')

df = pd.read_csv(
    csv_path,
    sep=';'
)

numeric_cols = [
    'temperature',
    'feels_like',
    'humidity',
    'wind_speed'
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors='coerce'
        )

df['state_name'] = df['city'].map(city_to_state)

df = df.dropna(
    subset=['state_name', 'temperature']
)

state_df = (
    df.groupby(
        'state_name',
        as_index=False
    )['temperature']
    .mean()
)

g = geocoder.ip('me')

user_city = g.city

if user_city:

    city_df = df[
        df['city'].str.lower() == user_city.lower()
    ]

    if city_df.empty:
        latest = df.iloc[-1]

    else:
        latest = city_df.iloc[-1]

else:
    latest = df.iloc[-1]

st.markdown(
    """
    <div class="title">
        🌦️ SKYDATA
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Real-Time Weather Monitoring System
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        '🌡️ Temperature',
        f"{latest['temperature']:.1f}°C"
    )

with col2:
    st.metric(
        '💧 Humidity',
        f"{latest['humidity']}%"
    )

with col3:
    st.metric(
        '🌬️ Wind Speed',
        f"{latest['wind_speed']} m/s"
    )

with col4:
    st.metric(
        '📍 City',
        latest['city']
    )

if geojson_path.exists():
    with open(
        geojson_path,
        'r',
        encoding='utf-8'
    ) as f:

        brazil_geojson = json.load(f)

    fig = go.Figure(
        go.Choropleth(
            geojson=brazil_geojson,

            locations=state_df['state_name'],

            z=state_df['temperature'],

            featureidkey='properties.name',

            colorscale='Turbo',

            marker_line_color='white',
            marker_line_width=1,

            customdata=state_df[['state_name']],

            hovertemplate=
            '<b>%{customdata[0]}</b><br>' +
            'Temperature: %{z:.1f}°C' +
            '<extra></extra>',

            colorbar_title='°C'
        )
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',

        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(
            color='white',
            size=14
        ),

        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        ),

        height=800
    )

    fig.update_geos(
        fitbounds='locations',
        visible=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
else:
<<<<<<< HEAD
    st.info('Map visualization will be available once brazil_states.geojson is added.')
=======
    st.info('Map visualization will be available once brazil_states.geojson is added.')
>>>>>>> d36a605 (new version)
