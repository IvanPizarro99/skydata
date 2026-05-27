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
    'Rio de Janeiro': 'Rio de Janeiro',
    'São Paulo': 'São Paulo',
    'Belo Horizonte': 'Minas Gerais',
    'Porto Alegre': 'Rio Grande do Sul',
    'Brasília': 'Distrito Federal',
    'Salvador': 'Bahia',
    'Fortaleza': 'Ceará',
    'Recife': 'Pernambuco',
    'Curitiba': 'Paraná',
    'Manaus': 'Amazonas'
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
    st.error('brazil_states.geojson not found.')
    st.stop()

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