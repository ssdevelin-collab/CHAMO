# accounts/utils.py
# Função que converte endereço em latitude/longitude usando OpenStreetMap (gratuito)

import requests

def geocodificar_endereco(endereco: str, cidade: str) -> tuple:
    """
    Recebe endereço e cidade, retorna (latitude, longitude) ou (None, None) se falhar.
    
    Uso:
        lat, lng = geocodificar_endereco("Rua das Flores, 123", "Salvador")
    """
    try:
        query = f"{endereco}, {cidade}, Brasil"
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 1,
        }
        headers = {
            # Nominatim exige um User-Agent identificando sua aplicação
            'User-Agent': 'Chamo-App/1.0'
        }
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()

        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Erro na geocodificação: {e}")

    return None, None