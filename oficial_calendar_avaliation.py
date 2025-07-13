from func_aux import avaliar_calendario, distancias, ler_csv

primeiro_turno = [
    # 1ª rodada
    {"Flamengo":"Internacional","Vasco":"Santos","Palmeiras":"Botafogo",
     "São Paulo":"Sport","RB Bragantino":"Ceará","Cruzeiro":"Mirassol",
     "Grêmio":"Atlético-MG","Bahia":"Corinthians","Fortaleza":"Fluminense",
     "Juventude":"Vitória"},
    # 2ª rodada
    {"Fluminense":"RB Bragantino","Botafogo":"Juventude",
     "Corinthians":"Vasco","Santos":"Bahia","Mirassol":"Fortaleza",
     "Atlético-MG":"São Paulo","Internacional":"Cruzeiro","Vitória":"Flamengo",
     "Ceará":"Grêmio","Sport":"Palmeiras"},
    # 3ª rodada
    {"Fluminense":"Santos","Vasco":"Sport","Palmeiras":"Corinthians",
     "São Paulo":"Cruzeiro","RB Bragantino":"Botafogo",
     "Atlético-MG":"Vitória","Grêmio":"Flamengo","Bahia":"Mirassol",
     "Fortaleza":"Internacional","Juventude":"Ceará"},
    # 4ª rodada
    {"Flamengo":"Juventude","Botafogo":"São Paulo","Corinthians":"Fluminense",
     "Santos":"Atlético-MG","Mirassol":"Grêmio","Cruzeiro":"Bahia",
     "Internacional":"Palmeiras","Vitória":"Fortaleza","Ceará":"Vasco",
     "Sport":"RB Bragantino"},
    # 5ª rodada
    {"Fluminense":"Vitória","Vasco":"Flamengo","Corinthians":"Sport",
     "São Paulo":"Santos","RB Bragantino":"Cruzeiro",
     "Atlético-MG":"Botafogo","Grêmio":"Internacional","Bahia":"Ceará",
     "Fortaleza":"Palmeiras","Juventude":"Mirassol"},
    # 6ª rodada
    {"Flamengo":"Corinthians","Botafogo":"Fluminense","Palmeiras":"Bahia",
     "Santos":"RB Bragantino","Mirassol":"Atlético-MG","Cruzeiro":"Vasco",
     "Internacional":"Juventude","Vitória":"Grêmio","Ceará":"São Paulo",
     "Sport":"Fortaleza"},
    # 7ª rodada
    {"Fluminense":"Sport","Vasco":"Palmeiras","Corinthians":"Internacional",
     "São Paulo":"Fortaleza","RB Bragantino":"Mirassol",
     "Cruzeiro":"Flamengo","Grêmio":"Santos","Bahia":"Botafogo",
     "Ceará":"Vitória","Juventude":"Atlético-MG"},
    # 8ª rodada
    {"Flamengo":"Bahia","Botafogo":"Internacional","Palmeiras":"São Paulo",
     "Santos":"Ceará","Mirassol":"Corinthians","Atlético-MG":"Fluminense",
     "Grêmio":"RB Bragantino","Vitória":"Vasco","Fortaleza":"Juventude",
     "Sport":"Cruzeiro"},
    # 9ª rodada
    {"Flamengo":"Botafogo","Vasco":"Fortaleza","Corinthians":"Santos",
     "São Paulo":"Grêmio","RB Bragantino":"Palmeiras",
     "Cruzeiro":"Atlético-MG","Internacional":"Mirassol","Bahia":"Vitória",
     "Ceará":"Sport","Juventude":"Fluminense"},
    # 10ª rodada
    {"Fluminense":"Vasco","Botafogo":"Ceará","Palmeiras":"Flamengo",
     "São Paulo":"Mirassol","RB Bragantino":"Juventude",
     "Atlético-MG":"Corinthians","Grêmio":"Bahia","Vitória":"Santos",
     "Fortaleza":"Cruzeiro","Sport":"Internacional"},
    # 11ª rodada
    {"Flamengo":"Fortaleza","Vasco":"RB Bragantino","Corinthians":"Vitória",
     "Santos":"Botafogo","Mirassol":"Sport","Cruzeiro":"Palmeiras",
     "Internacional":"Fluminense","Bahia":"São Paulo","Ceará":"Atlético-MG",
     "Juventude":"Grêmio"},
    # 12ª rodada
    {"Fluminense":"Ceará","Botafogo":"Mirassol","Palmeiras":"Juventude",
     "São Paulo":"Vasco","RB Bragantino":"Bahia","Atlético-MG":"Internacional",
     "Grêmio":"Corinthians","Vitória":"Cruzeiro","Fortaleza":"Santos",
     "Sport":"Flamengo"},
    # 13ª rodada
    {"Flamengo":"São Paulo","Vasco":"Botafogo","Corinthians":"RB Bragantino",
     "Santos":"Palmeiras","Mirassol":"Fluminense","Cruzeiro":"Grêmio",
     "Internacional":"Vitória","Bahia":"Atlético-MG","Fortaleza":"Ceará",
     "Juventude":"Sport"},
    # 14ª rodada
    {"Fluminense":"Cruzeiro","Botafogo":"Vitória","Palmeiras":"Mirassol",
     "Santos":"Flamengo","RB Bragantino":"São Paulo","Atlético-MG":"Sport",
     "Grêmio":"Fortaleza","Bahia":"Internacional","Ceará":"Corinthians",
     "Juventude":"Vasco"},
    # 15ª rodada
    {"Flamengo":"Fluminense","Vasco":"Grêmio","Palmeiras":"Atlético-MG",
     "São Paulo":"Corinthians","Mirassol":"Santos","Cruzeiro":"Juventude",
     "Internacional":"Ceará","Vitória":"RB Bragantino",
     "Fortaleza":"Bahia","Sport":"Botafogo"},
    # 16ª rodada
    {"Fluminense":"Palmeiras","Vasco":"Bahia","Corinthians":"Cruzeiro",
     "Santos":"Internacional","RB Bragantino":"Flamengo",
     "Atlético-MG":"Fortaleza","Grêmio":"Botafogo","Vitória":"Sport",
     "Ceará":"Mirassol","Juventude":"São Paulo"},
    # 17ª rodada
    {"Flamengo":"Atlético-MG","Botafogo":"Corinthians","Palmeiras":"Grêmio",
     "São Paulo":"Fluminense","Mirassol":"Vitória","Cruzeiro":"Ceará",
     "Internacional":"Vasco","Bahia":"Juventude","Fortaleza":"RB Bragantino",
     "Sport":"Santos"},
    # 18ª rodada
    {"Fluminense":"Grêmio","Botafogo":"Cruzeiro","Corinthians":"Fortaleza",
     "Santos":"Juventude","Mirassol":"Vasco","Atlético-MG":"RB Bragantino",
     "Internacional":"São Paulo","Vitória":"Palmeiras","Ceará":"Flamengo",
     "Sport":"Bahia"},
    # 19ª rodada
    {"Flamengo":"Mirassol","Vasco":"Atlético-MG","Palmeiras":"Ceará",
     "São Paulo":"Vitória","RB Bragantino":"Internacional",
     "Cruzeiro":"Santos","Grêmio":"Sport","Bahia":"Fluminense",
     "Fortaleza":"Botafogo","Juventude":"Corinthians"}
]

categorias = {
    'A': ['Botafogo', 'Palmeiras', 'Flamengo', 'Fortaleza'],
    'B': ['Internacional', 'São Paulo', 'Corinthians', 'Bahia', 'Cruzeiro', 'Vasco'],
    'C': ['Vitória', 'Atlético-MG', 'Fluminense', 'Grêmio', 'Juventude', 'RB Bragantino'],
    'D': ['Santos', 'Mirassol', 'Sport', 'Ceará']
}
categorias_ptime = {t: cat for cat, times_cat in categorias.items() for t in times_cat}

# leitura dos arquivos
nomes_linhas, nomes_colunas, df_times = ler_csv("data/matriz_distancias_brasileirao_2025.csv")
indice_times = {nome: i for i, nome in enumerate(nomes_linhas)}
times = nomes_linhas
numero_times = len(times)
rodadas_pturno = numero_times - 1
rodadas_total = rodadas_pturno * 2

# Gerando returno invertido
segundo_turno = [{fora: casa for casa, fora in rd.items()} for rd in primeiro_turno]
calendario = primeiro_turno + segundo_turno


dist_total = distancias(calendario, df_times, indice_times)
fitness = avaliar_calendario(calendario, times, df_times, indice_times, categorias_ptime, numero_times, rodadas_total)
print(f"Distância total percorrida pelos times no campeonato: {dist_total:.2f} km")
print(f"Fitness: {fitness}")