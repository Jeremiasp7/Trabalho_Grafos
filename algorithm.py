from func_aux import ler_csv, atualizar_historico_confrontos, gerar_emparelhamento, distancias, avaliar_calendario, exibir_calendario, gerar_rodada 

# leitura dos arquivos
nomes_linhas, nomes_colunas, df_times = ler_csv("data/matriz_distancias_brasileirao_2025.csv")
indice_times = {nome: i for i, nome in enumerate(nomes_linhas)}
times = nomes_linhas
numero_times = len(times)

# parâmetros iniciais
rodadas_pturno = numero_times - 1
rodadas_total = rodadas_pturno * 2
tipos_supermatches = ['tipo-1', 'tipo-2', 'tipo-3']

# categorias de times
categorias = {
    'A': ['Botafogo', 'Palmeiras', 'Flamengo', 'Fortaleza'],
    'B': ['Internacional', 'São Paulo', 'Corinthians', 'Bahia', 'Cruzeiro', 'Vasco'],
    'C': ['Vitória', 'Atlético-MG', 'Fluminense', 'Grêmio', 'Juventude', 'RB Bragantino'],
    'D': ['Santos', 'Mirassol', 'Sport', 'Ceará']
}
categorias_ptime = {t: cat for cat, times_cat in categorias.items() for t in times_cat}

# =========== GERAÇÃO DO CALENDÁRIO ===========
def gerar_calendario(max_tentativas=30):
    for _ in range(max_tentativas):
        calendario = []
        rodadas_previas = []
        historico_confrontos = {}
        mandos_anteriores = {}
        confrontos_realizados = set()

        sucesso = True

        for r in range(rodadas_pturno):
            emp = gerar_emparelhamento(df_times, rodadas_previas, r, historico_confrontos, numero_times, times, indice_times, categorias_ptime, confrontos_realizados)
            if not emp:
                sucesso = False
                break
            rodada = gerar_rodada(emp, r, mandos_anteriores)
            atualizar_historico_confrontos(rodada, r, historico_confrontos, indice_times, df_times)

            for casa, fora in rodada.items():
                confronto = tuple(sorted((casa, fora)))
                confrontos_realizados.add(confronto)

            rodadas_previas.append(rodada)
            calendario.append(rodada)

        if not sucesso:
            continue  # tenta novamente do zero

        # Segundo turno espelhado
        for r in range(rodadas_pturno):
            rodada_espelho = {fora: casa for casa, fora in calendario[r].items()}
            calendario.append(rodada_espelho)

        return calendario  # sucesso

    raise Exception("Não foi possível gerar um calendário viável após várias tentativas.")

# =========== MAIN ===========
if __name__ == "__main__":
   calendario = gerar_calendario()
   exibir_calendario(calendario)

   fitness = avaliar_calendario(calendario, times, df_times, indice_times, categorias_ptime, numero_times, rodadas_total)
   print(f"Fitness: {fitness}")

   distancia_total = distancias(calendario, df_times, indice_times)
   print(f"Distância total percorrida pelos times no campeonato: {distancia_total:.2f} km")

