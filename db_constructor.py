# importações
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time
import os

# times que disputam o brasileirão 2025 e suas respectivas cidades
times_cidades = {
    "Atlético-MG": "Belo Horizonte",
    "Bahia": "Salvador",
    "Botafogo": "Rio de Janeiro",
    "Ceará": "Fortaleza",
    "Corinthians": "São Paulo",
    "Cruzeiro": "Belo Horizonte",
    "Flamengo": "Rio de Janeiro",
    "Fluminense": "Rio de Janeiro",
    "Fortaleza": "Fortaleza",
    "Juventude": "Caxias do Sul",
    "Grêmio": "Porto Alegre",
    "Internacional": "Porto Alegre",
    "Mirassol": "Mirassol",
    "Palmeiras": "São Paulo",
    "RB Bragantino": "Bragança Paulista",
    "Santos": "Santos",
    "São Paulo": "São Paulo",
    "Sport": "Recife",
    "Vasco": "Rio de Janeiro",
    "Vitória": "Salvador"
}

# inicializa o geolocalizador com um agente de usuário específico.
geolocator = Nominatim(user_agent="brasileirao_distance_matrix")
coordenadas = {}

for cidade in set(times_cidades.values()):
    # obtém as coordenadas da cidade usando o geolocalizador.
    location = geolocator.geocode(f"{cidade}, Brasil")
    if location:
        coordenadas[cidade] = (location.latitude, location.longitude)
    else:
        print(f"Não foi possível encontrar coordenadas para: {cidade}")
    time.sleep(1)  # evitar sobrecarga na API gratuita

# cria uma lista com os nomes dos times.
times = list(times_cidades.keys())
# cria um DataFrame (matriz) com os nomes dos times como índices e colunas, preenchido inicialmente com None.
matriz_distancia = pd.DataFrame(index=times, columns=times)

# preencher a matriz de distâncias
for time1 in times:
    cidade1 = times_cidades[time1]
    for time2 in times:
        cidade2 = times_cidades[time2]
        if cidade1 == cidade2:
            distancia = 0
        # se os times forem de cidades diferentes, calcula a distância geodésica.
        else:
            # obtém as coordenadas das cidades.
            coords1 = coordenadas[cidade1]
            coords2 = coordenadas[cidade2]
            # calcula a distância geodésica em quilômetros e arredonda para 1 casa decimal.
            distancia = round(geodesic(coords1, coords2).kilometers, 1)
        # atribui a distância calculada à posição correspondente na matriz.
        matriz_distancia.at[time1, time2] = distancia

caminho_relativo = os.path.join('data', 'matriz_distancias_brasileirao_2025.csv')
matriz_distancia.to_csv(caminho_relativo)