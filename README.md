# 📅 Gerador de Calendário do Brasileirão 2025

Este projeto tem como objetivo gerar um **calendário de partidas** para o Campeonato Brasileiro de Futebol 2025 (Brasileirão), considerando **restrições logísticas e esportivas** como:

- Minimização de distâncias percorridas pelos times
- Evitar sequências longas de jogos em casa ou fora
- Evitar clássicos com rodadas muito próximas
- Evitar sequência de confrontos contra times da mesma categoria

## ⚙️ Funcionalidades

- Geração automática de emparelhamentos viáveis para cada rodada
- Espelhamento do primeiro turno para formar o segundo turno
- Avaliação do calendário com métricas de fitness
- Geração e exportação de matriz de distâncias geográficas entre cidades dos times
- Respeito a diversas restrições esportivas

---

## 📁 Estrutura do Projeto
```
├── data/
│ └── matriz_distancias_brasileirao_2025.csv
├── func_aux.py # todas as funções auxiliares
├── algorithm.py # ponto de entrada principal
├── db_constructor.py
├── oficial_calendar_avaliation.py
└── README.md
```

---

## 📦 Requisitos

- Python 3.8+
- Bibliotecas necessárias:

```bash
pip install pandas geopy
```
🚀 Como Executar
1. Gere a matriz de distâncias

O primeiro passo é gerar a matriz de distâncias geográficas entre as cidades dos times participantes:

python main.py

Este passo irá:

  - Usar o geopy para consultar as coordenadas de cada cidade

  - Calcular a distância geodésica entre todas as cidades

  - Gerar o arquivo data/matriz_distancias_brasileirao_2025.csv

  ⚠️ Atenção: Este processo pode demorar alguns minutos pois há um sleep(1) para evitar sobrecarregar a API gratuita do Nominatim.

2. Execute o gerador de calendário

Após a geração da matriz de distâncias, o calendário pode ser gerado com:

python main.py

A saída exibirá:

  - O calendário completo de rodadas

  - O fitness do calendário gerado

  - A distância total percorrida pelos times

📊 Critérios de Avaliação (Fitness)

O fitness do calendário é calculado com base nos seguintes critérios:

  - Distância total percorrida

  - Penalidades por mando de campo repetido

  - Clássicos em rodadas próximas

  - Três confrontos consecutivos contra a mesma categoria

  O objetivo do algoritmo é maximizar o fitness (valor entre 0 e 1).

🏷️ Categorias dos Times

Os times são agrupados nas seguintes categorias para controle de restrições:

- A: Botafogo, Palmeiras, Flamengo, Fortaleza

- B: Internacional, São Paulo, Corinthians, Bahia, Cruzeiro, Vasco

- C: Vitória, Atlético-MG, Fluminense, Grêmio, Juventude, RB Bragantino

- D: Santos, Mirassol, Sport, Ceará

✅ Exemplo de Saída

📅 CALENDÁRIO DE JOGOS
```
Rodada 01
------------------------------
Botafogo        x Bahia
Palmeiras       x Vasco
...

Fitness: 0.8923
Distância total percorrida pelos times no campeonato: 132543.7 km
```
📌 Observações

    O algoritmo pode rodar várias vezes até encontrar um calendário viável (máximo de 30 tentativas).

    O código é modularizado, podendo ser adaptado para outros formatos de competições.
