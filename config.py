"""Configurações centralizadas do projeto SkyData"""

# Cidades e estados do Brasil
CITIES = {
    'Rio Branco': 'AC', 'Maceió': 'AL', 'Macapá': 'AP', 'Manaus': 'AM',
    'Salvador': 'BA', 'Fortaleza': 'CE', 'Brasília': 'DF', 'Vitória': 'ES',
    'Goiânia': 'GO', 'São Luís': 'MA', 'Cuiabá': 'MT', 'Campo Grande': 'MS',
    'Belo Horizonte': 'MG', 'Belém': 'PA', 'João Pessoa': 'PB', 'Curitiba': 'PR',
    'Recife': 'PE', 'Teresina': 'PI', 'Rio de Janeiro': 'RJ', 'Natal': 'RN',
    'Porto Alegre': 'RS', 'Porto Velho': 'RO', 'Boa Vista': 'RR',
    'Joinville': 'SC', 'São Paulo': 'SP', 'Aracaju': 'SE', 'Palmas': 'TO',
}

CITY_TO_STATE = {
    'Rio Branco': 'Acre', 'Maceió': 'Alagoas', 'Macapá': 'Amapá',
    'Manaus': 'Amazonas', 'Salvador': 'Bahia', 'Fortaleza': 'Ceará',
    'Brasília': 'Distrito Federal', 'Vitória': 'Espírito Santo',
    'Goiânia': 'Goiás', 'São Luís': 'Maranhão', 'Cuiabá': 'Mato Grosso',
    'Campo Grande': 'Mato Grosso do Sul', 'Belo Horizonte': 'Minas Gerais',
    'Belém': 'Pará', 'João Pessoa': 'Paraíba', 'Curitiba': 'Paraná',
    'Recife': 'Pernambuco', 'Teresina': 'Piauí', 'Rio de Janeiro': 'Rio de Janeiro',
    'Natal': 'Rio Grande do Norte', 'Porto Alegre': 'Rio Grande do Sul',
    'Porto Velho': 'Rondônia', 'Boa Vista': 'Roraima', 'Joinville': 'Santa Catarina',
    'São Paulo': 'São Paulo', 'Aracaju': 'Sergipe', 'Palmas': 'Tocantins',
}

APP_NAME = 'SkyData'
DATA_DIR = 'data'
CSV_FILE = f'{DATA_DIR}/weather.csv'
GEOJSON_FILE = f'{DATA_DIR}/brazil_states.geojson'
