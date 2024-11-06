from flask import Flask, jsonify, request,send_from_directory
import requests
import os

app = Flask(__name__)

# Obter a API Key da variável de ambiente
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

app = Flask(__name__)


@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# Rota para servir arquivos estáticos (CSS e JavaScript)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

# Variável de ambiente para chave da API
API_KEY = os.getenv("API_KEY")
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({"error": "Parâmetros 'lat' e 'lon' são necessários"}), 400

    # Monta a URL da API do Weatherbit
    weather_url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={API_KEY}"
    
    # Faz a requisição à API do Weatherbit
    response = requests.get(weather_url)
    if response.status_code == 200:
        weather_data = response.json()
        
        # Extrai e organiza os dados necessários para o frontend
        if 'data' in weather_data and len(weather_data['data']) > 0:
            data = weather_data['data'][0]
            formatted_data = {
                "name": data.get("city_name"),
                "main": {
                    "temp": data.get("temp"),
                    "temp_max": data.get("max_temp", data.get("temp")),  # A API pode não ter temp_max, usando temp como fallback
                    "temp_min": data.get("min_temp", data.get("temp"))   # A API pode não ter temp_min, usando temp como fallback
                },
                "weather": [{
                    "description": data.get("weather", {}).get("description")
                }]
            }
            return jsonify(formatted_data)
        else:
            return jsonify({"error": "Dados de clima não encontrados na resposta"}), 500
    else:
        return jsonify({"error": "Não foi possível obter os dados de clima"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)