async function fetchWeather(lat, lon) {
    const url = `/api/weather/current?lat=${lat}&lon=${lon}`;
    console.log('coordenadas recebidas latitude: ',lat)
    console.log('coordenadas recebidas longitude: ',lon)
    const response = await fetch(url);
    const data = await response.json();
    // Log para verificar a resposta completa da API
    console.log("Resposta da API de clima:", data);
    return data;
}

function updateWeather(data) {
    document.getElementById('city-name').textContent = data.name;
    document.getElementById('temperature').textContent = `${data.main.temp.toFixed(0)}°C`;
    document.getElementById('weather-description').textContent = data.weather[0].description;
    document.getElementById('max-min').textContent = `Máx.: ${data.main.temp_max.toFixed(0)}° Mín.: ${data.main.temp_min.toFixed(0)}°`;

    if (data.main.temp > 40) {
        document.getElementById('weather-alert').textContent = 'Advertência de calor excessivo';
    } else {
        document.getElementById('weather-alert').textContent = 'Sem alertas no momento.';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                // Chama a API com a localização do usuário
                fetchWeather(lat, lon).then(data => updateWeather(data));
            },
            (error) => {
                console.error("Erro ao obter localização:", error);
                document.getElementById('city-name').textContent = "Localização não encontrada";
            }
        );
    } else {
        document.getElementById('city-name').textContent = "Geolocalização não suportada";
    }
});
