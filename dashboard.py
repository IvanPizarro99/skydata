import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from pathlib import Path
import geocoder

st.set_page_config(
    page_title='SkyData Dashboard',
    layout='wide'
)

# City to State Mapping
city_to_state = {
    'Rio Branco': 'Acre', 'Cruzeiro do Sul': 'Acre',
    'Maceió': 'Alagoas', 'Rio Largo': 'Alagoas',
    'Macapá': 'Amapá', 'Santana': 'Amapá',
    'Manaus': 'Amazonas', 'Parintins': 'Amazonas',
    'Salvador': 'Bahia', 'Feira de Santana': 'Bahia', 'Vitória da Conquista': 'Bahia', 'Ilhéus': 'Bahia', 'Jequié': 'Bahia',
    'Fortaleza': 'Ceará', 'Caucaia': 'Ceará', 'Juazeiro do Norte': 'Ceará', 'Sobral': 'Ceará',
    'Brasília': 'Distrito Federal',
    'Vitória': 'Espírito Santo', 'Vila Velha': 'Espírito Santo', 'Serra': 'Espírito Santo',
    'Goiânia': 'Goiás', 'Aparecida de Goiânia': 'Goiás', 'Anápolis': 'Goiás',
    'São Luís': 'Maranhão', 'Imperatriz': 'Maranhão', 'Caxias': 'Maranhão',
    'Cuiabá': 'Mato Grosso', 'Várzea Grande': 'Mato Grosso', 'Rondonópolis': 'Mato Grosso',
    'Campo Grande': 'Mato Grosso do Sul', 'Dourados': 'Mato Grosso do Sul', 'Três Lagoas': 'Mato Grosso do Sul',
    'Belo Horizonte': 'Minas Gerais', 'Uberlândia': 'Minas Gerais', 'Contagem': 'Minas Gerais', 'Juiz de Fora': 'Minas Gerais', 'Divinópolis': 'Minas Gerais',
    'Belém': 'Pará', 'Ananindeua': 'Pará', 'Marabá': 'Pará', 'Santarém': 'Pará',
    'João Pessoa': 'Paraíba', 'Campina Grande': 'Paraíba', 'Patos': 'Paraíba',
    'Curitiba': 'Paraná', 'Londrina': 'Paraná', 'Maringá': 'Paraná', 'Ponta Grossa': 'Paraná',
    'Recife': 'Pernambuco', 'Jaboatão dos Guararapes': 'Pernambuco', 'Olinda': 'Pernambuco', 'Caruaru': 'Pernambuco',
    'Teresina': 'Piauí', 'Parnaíba': 'Piauí', 'Picos': 'Piauí',
    'Rio de Janeiro': 'Rio de Janeiro', 'Niterói': 'Rio de Janeiro', 'Duque de Caxias': 'Rio de Janeiro', 'São Gonçalo': 'Rio de Janeiro',
    'Natal': 'Rio Grande do Norte', 'Mossoró': 'Rio Grande do Norte', 'Parnamirim': 'Rio Grande do Norte',
    'Porto Alegre': 'Rio Grande do Sul', 'Caxias do Sul': 'Rio Grande do Sul', 'Pelotas': 'Rio Grande do Sul', 'Santa Maria': 'Rio Grande do Sul',
    'Porto Velho': 'Rondônia', 'Ariquemes': 'Rondônia', 'Ji-Paraná': 'Rondônia',
    'Boa Vista': 'Roraima', 'Rorainópolis': 'Roraima',
    'Joinville': 'Santa Catarina', 'Blumenau': 'Santa Catarina', 'Florianópolis': 'Santa Catarina', 'Chapecó': 'Santa Catarina',
    'São Paulo': 'São Paulo', 'Guarulhos': 'São Paulo', 'Campinas': 'São Paulo', 'São Bernardo do Campo': 'São Paulo', 'Santo André': 'Santo André',
    'Aracaju': 'Sergipe', 'Nossa Senhora do Socorro': 'Sergipe',
    'Palmas': 'Tocantins', 'Araguaína': 'Tocantins',
}

# Custom CSS Layout
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

@st.cache_data
def load_weather_data(path):
    if not path.exists():
        return None
    data = pd.read_csv(path, sep=';')
    
    # Safely convert and combine Date and Time into a datetime object
    if 'date' in data.columns and 'time' in data.columns:
        data['timestamp'] = pd.to_datetime(
            data['date'] + ' ' + data['time'], 
            format='%d/%m/%Y %H:%M:%S', 
            errors='coerce'
        )
    
    numeric_cols = ['temperature', 'feels_like', 'humidity', 'wind_speed']
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    return data

@st.cache_data
def load_geojson_data(path):
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

df = load_weather_data(csv_path)
brazil_geojson = load_geojson_data(geojson_path)

if df is None:
    st.error('weather.csv not found.')
    st.stop()

df['state_name'] = df['city'].map(city_to_state)
df = df.dropna(subset=['state_name', 'temperature'])

if df.empty:
    st.error('No valid weather data available to display.')
    st.stop()

# Generate a snapshot containing only the absolute latest record for each city
latest_snapshot = df.sort_values('timestamp').drop_duplicates('city', keep='last')

# Calculate state average temperatures using the latest snapshot data
state_df = latest_snapshot.groupby('state_name', as_index=False)['temperature'].mean()

# Location selection controller
available_cities = sorted(df['city'].unique())
default_city = available_cities[0] if available_cities else ""
try:
    g = geocoder.ip('me')
    if g.city and g.city in available_cities:
        default_city = g.city
except Exception:
    pass

st.markdown('<div class="title">SKYDATA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-Time Weather Monitoring System</div>', unsafe_allow_html=True)

selected_city = st.selectbox(
    'Select a city to explore:',
    options=available_cities,
    index=available_cities.index(default_city) if default_city in available_cities else 0
)

# Extract specific details for KPI display
city_latest = latest_snapshot[latest_snapshot['city'] == selected_city]
latest = city_latest.iloc[-1] if not city_latest.empty else latest_snapshot.iloc[-1]

# Top KPI Layout Metrics Display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Temperature', f"{latest['temperature']:.1f}°C")
with col2:
    st.metric('Humidity', f"{latest['humidity']}%")
with col3:
    st.metric('Wind Speed', f"{latest['wind_speed']} m/s")
with col4:
    st.metric('Condition', str(latest['weather']).title())

st.markdown('---')

# Organized Dashboard Tabs View
tab1, tab2 = st.tabs(['National Map Overview', 'Analytical Insights and Trends'])

with tab1:
    if brazil_geojson:
        # Map using semantic 'Thermal' scale and smoother borders
        fig_map = go.Figure(
            go.Choropleth(
                geojson=brazil_geojson,
                locations=state_df['state_name'],
                z=state_df['temperature'],
                featureidkey='properties.name',
                colorscale='Thermal',
                marker_line_color='rgba(255,255,255,0.2)',
                marker_line_width=1,
                customdata=state_df[['state_name']],
                hovertemplate='<b>%{customdata[0]}</b><br>Average Temperature: %{z:.1f}°C<extra></extra>',
                colorbar_title='°C'
            )
        )
        fig_map.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            margin=dict(l=0, r=0, t=10, b=0),
            height=700
        )
        fig_map.update_geos(fitbounds='locations', visible=False)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info('Map visualization will be available once brazil_states.geojson is added.')

with tab2:
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        # Time-Series Line Chart for the Selected City
        city_history = df[df['city'] == selected_city].sort_values('timestamp')
        if len(city_history) > 0:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=city_history['timestamp'],
                y=city_history['temperature'],
                mode='lines+markers',
                line=dict(color='#38bdf8', width=3),
                marker=dict(size=6, color='#0ea5e9'),
                name='Temperature'
            ))
            fig_line.update_layout(
                title=dict(text=f"Temperature Trend over Time: {selected_city}", font=dict(size=18)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='°C'),
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info('Not enough chronological data points to render a historical line timeline chart yet.')
            
    with chart_col2:
        # Horizontal Bar Chart Ranking Extremes
        top_hottest = latest_snapshot.sort_values('temperature', ascending=False).head(5)
        
        fig_bar = go.Figure(go.Bar(
            x=top_hottest['temperature'],
            y=top_hottest['city'],
            orientation='h',
            marker=dict(
                color=top_hottest['temperature'],
                colorscale='YlOrRd'
            ),
            hovertemplate='<b>%{y}</b><br>Temperature: %{x:.1f}°C<extra></extra>'
        ))
        fig_bar.update_layout(
            title=dict(text="Top 5 Hottest Cities", font=dict(size=18)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False, title='°C'),
            yaxis=dict(autorange="reversed"),
            margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)