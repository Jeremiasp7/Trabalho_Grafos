# =========== FUNÇÕES AUXILIARES ===========
def ler_csv(caminho):
  with open(caminho, 'r', encoding='utf-8') as arquivo:
    linhas = [linha.strip().split(',') for linha in arquivo if linha.strip()]
    
  colunas = linhas[0][1:]
  nomes = []
  matriz = []

  for linha in linhas[1:]:
    nome_linha = linha[0]
    valores = [float(v) for v in linha[1:]]
    nomes.append(nome_linha)
    matriz.append(valores)
  
  return nomes, colunas, matriz

class LCG:
    def __init__(self, seed=1):
        self.mod = 2**31 - 1
        self.a = 1103515245
        self.c = 12345
        self.state = seed
        
    def next(self):
        self.state = (self.a * self.state + self.c) % self.mod
        return self.state

    def randrange(self, limite):
        return self.next() % limite

def shuffle_lista_lcg(lista, seed):
    rng = LCG(seed)
    n = len(lista)
    for i in range(n - 1, 0, -1):
        j = rng.randrange(i + 1)
        lista[i], lista[j] = lista[j], lista[i]

# =========== RESTRIÇÕES DIRETAS ===========
def conflito_categoria(rodadas, t1, t2, categorias_ptime):
  # evita mais de 2 confrontos consecutivos contra mesma categoria
  if not rodadas:
    return False
  cat1 = categorias_ptime[t1]
  cat2 = categorias_ptime[t2]
  for r in reversed(rodadas[-2:]):
    if (t1 in r and categorias_ptime[r[t1]] == cat1) or \
        (t2 in r and categorias_ptime[r[t2]] == cat2):
      return True
  return False

def conflito_classicos(t1, t2, rodada_atual, historico_confrontos, df_times, indice_times, intervalo=2):
  if df_times[indice_times[t1]][indice_times[t2]] > 0:
    return False  # só se aplica se são da mesma cidade
  # Verifica se t1 ou t2 enfrentaram outro time da mesma cidade recentemente
  for adversario, r in historico_confrontos.get(t1, []):
    if df_times[indice_times[t1]][indice_times[adversario]] == 0 and rodada_atual - r < intervalo:
      return True
  for adversario, r in historico_confrontos.get(t2, []):
    if df_times[indice_times[t2]][indice_times[adversario]] == 0 and rodada_atual - r < intervalo:
      return True

def conflito_mando(time, rodada_idx, mandos_time, mandante):
  if rodada_idx < 2:
    return False
  ultimos_mandos = mandos_time[time][-2:] if time in mandos_time else []
  if len(ultimos_mandos) < 2:
    return False
  sequencia = ultimos_mandos + ['casa' if mandante else 'fora']
  return sequencia[0] == sequencia[1] == sequencia[2]

# =========== HISTÓRICO DE CONFRONTOS ===========
def atualizar_historico_confrontos(rodada, rodada_atual, historico, indice_times, df_times):
  for casa, fora in rodada.items():
    if df_times[indice_times[casa]][indice_times[fora]] == 0:
      historico.setdefault(casa, []).append((fora, rodada_atual))
      historico.setdefault(fora, []).append((casa, rodada_atual))

# =========== EMPARELHAMENTO DE UMA RODADA ===========
def gerar_emparelhamento(df_times, rodadas_previas, rodada_atual, historico_confrontos, numero_times, times, indice_times, categorias_ptime, confrontos_realizados=None, max_tentativas=100,):
    pares = []
    n = numero_times
    for i in range(n):
      for j in range(i + 1, n):
        pares.append((times[i], times[j]))
    pares.sort(key=lambda x: df_times[indice_times[x[0]]][indice_times[x[1]]])

    for super_matches in range(3):  # 0 = tudo, 1 = sem categoria, 2 = sem clássicos
        for tentativa in range(max_tentativas):
            seed = tentativa + super_matches * max_tentativas  # ou outra fórmula para variar semente
            pares_random = pares[:]  # copia a lista
            shuffle_lista_lcg(pares_random, seed)

            emparelhamento = []
            usados = set()
            for t1, t2 in pares_random:
                if t1 in usados or t2 in usados:
                    continue
                if confrontos_realizados is not None and tuple(sorted((t1, t2))) in confrontos_realizados:
                    continue
                if super_matches < 2 and conflito_classicos(t1, t2, rodada_atual, historico_confrontos, df_times, indice_times):
                    continue
                if super_matches < 1 and conflito_categoria(rodadas_previas, t1, t2, categorias_ptime):
                    continue
                emparelhamento.append((t1, t2))
                usados.update([t1, t2])
                if len(emparelhamento) == numero_times // 2:
                    return emparelhamento

# =========== MÉTRICAS DE AVALIAÇÃO ===========
def distancias(calendario, df_times, indice_times):
    distancia_total = 0
    for rodada in calendario:
        for casa, fora in rodada.items():
            distancia_total += df_times[indice_times[casa]][indice_times[fora]]
    return distancia_total

def avaliar_calendario(calendario, times, df_times, indice_times, categorias_ptime, numero_times, rodadas_total):
    custo_total = 0
    penalidade_mando = 0
    penalidade_classico = 0
    penalidade_categoria = 0
    mandos = {t: [] for t in times}
    adversarios = {t: [] for t in times}
    rodadas_classicos = {t: [] for t in times}

    for rodada_idx, rodada in enumerate(calendario):
        for casa, fora in rodada.items():
            # Acumula distância
            custo_total += df_times[indice_times[casa]][indice_times[fora]]

            # Registro de mando
            mandos[casa].append('casa')
            mandos[fora].append('fora')

            # Registro de adversários
            adversarios[casa].append(fora)
            adversarios[fora].append(casa)

            # Verifica se é clássico (mesma cidade)
            if df_times[indice_times[casa]][indice_times[fora]] == 0:
                rodadas_classicos[casa].append(rodada_idx)
                rodadas_classicos[fora].append(rodada_idx)

    # Penalidade por mando consecutivo
    for t in times:
        i = 0
        while i < len(mandos[t]) - 2:
            count = 1
            while i + count < len(mandos[t]) and mandos[t][i] == mandos[t][i + count]:
                count += 1
            if count >= 3:
                penalidade_mando += (count - 2)
                i += count
            else:
                i += 1

    # Penalidade por clássicos com intervalo menor que 3 rodadas
    for t in times:
        rodadas = rodadas_classicos[t]
        for i in range(len(rodadas) - 1):
            if rodadas[i+1] - rodadas[i] < 3:
                penalidade_classico += 1

    # Penalidade por 3 confrontos consecutivos contra mesma categoria
    for t in times:
        categorias_seq = []
        for adv in adversarios[t]:
            categorias_seq.append(categorias_ptime[adv])
        for i in range(len(categorias_seq) - 2):
            if categorias_seq[i] == categorias_seq[i+1] == categorias_seq[i+2]:
                penalidade_categoria += 1

    # Normalização
    max_dist = max(max(linha) for linha in df_times)
    custo_maximo_possivel = max_dist * (numero_times // 2) * rodadas_total
    custo_normalizado = custo_total / custo_maximo_possivel

    # Penalidades normalizadas
    penalidade_total = penalidade_mando + penalidade_classico + penalidade_categoria
    penalidade_max_teorica = numero_times * (rodadas_total - 2)
    penalidade_normalizada = penalidade_total / penalidade_max_teorica

    # Pesos (ajustáveis)
    peso_distancia = 0.7
    peso_penalidade = 0.3

    fitness = 1 - (peso_distancia * custo_normalizado + peso_penalidade * penalidade_normalizada)
    fitness = max(0, min(1, fitness))

    return fitness

# =========== DETERMINAÇÃO DA RODADA ===========
def gerar_rodada(emparelhamento, rodada_idx, mandos_anteriores):
  rodada = {}

  for i, (t1, t2) in enumerate(emparelhamento):
    # tenta atribuir t1 como mandante primeiro
    if not conflito_mando(t1, rodada_idx, mandos_anteriores, True) and \
       not conflito_mando(t2, rodada_idx, mandos_anteriores, False):
      rodada[t1] = t2
      mandos_anteriores.setdefault(t1, []).append('casa')
      mandos_anteriores.setdefault(t2, []).append('fora')
    # caso contrário, tenta o inverso
    elif not conflito_mando(t2, rodada_idx, mandos_anteriores, True) and \
         not conflito_mando(t1, rodada_idx, mandos_anteriores, False):
      rodada[t2] = t1
      mandos_anteriores.setdefault(t2, []).append('casa')
      mandos_anteriores.setdefault(t1, []).append('fora')
    else:
      rodada[t1] = t2
      mandos_anteriores.setdefault(t1, []).append('casa')
      mandos_anteriores.setdefault(t2, []).append('fora')
  return rodada

# =========== EXIBIÇÃO DO CALENDÁRIO ===========
def exibir_calendario(calendario):
  print("\n📅 CALENDÁRIO DE JOGOS")
  for i, rodada in enumerate(calendario):
    print(f"\nRodada {i+1:02d}")
    print("-" * 30)
    usados = set()
    for casa, fora in rodada.items():
      if (casa not in usados) and (fora not in usados):
        print(f"{casa:<15} x {fora:<15}")
        usados.add(casa)
        usados.add(fora)