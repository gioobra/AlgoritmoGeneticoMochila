import random
import json
from pathlib import Path
import matplotlib.pyplot as plt

SEED_EXPERIMENTO = 0
LIMITE_DE_PESO = 0
TAMANHO_POPULACAO = 0
PESOS_DOS_ITENS = []
VALORES_DOS_ITENS = []
MAX_GERACOES = 100

def AGCanonico(populacao, n, r, pCross, pMut):
    '''
    n = quantidade da populacao (r = n normalmente)
    r = quantidade dos descendentes (r = n normalmente)
    pCross = probabilidade de crossover (0.8 tipico)
    pMut = probabilidade de mutacao (0.05 tipico)
    '''
    for cromossomo in populacao:
        Fitness(cromossomo)
    geracao = 0
    estagnado = 0


    historicoMelhorFitness = []
    historicoFitnessMedio = []

    while geracao < MAX_GERACOES and estagnado != 30:
        populacaoSelecionada = Roleta(populacao, r)
        descendentesCruzados = []
        velhoMelhor = Fitness(ObterMelhorCromossomo(populacao))

        for pai1,pai2 in AgruparEmPares(populacaoSelecionada):
            if (random.random() < pCross): # decide entre 0.0 e 1.0
                filho1, filho2 = Cruzar(pai1, pai2) 
            else: 
                filho1, filho2 = pai1, pai2
            descendentesCruzados.append(filho1)
            descendentesCruzados.append(filho2)
        
        descendentesMutados = []
        for cromossomo in descendentesCruzados:
            for i in range(len(cromossomo)):
                if(random.random() < pMut):
                    cromossomo[i] = Mutacao(cromossomo[i])
            descendentesMutados.append(cromossomo)
        
        populacaoTotal = populacao + descendentesMutados
        populacao = Melhores(populacaoTotal, n) 

        novoMelhor = Fitness(ObterMelhorCromossomo(populacao))
        
        somaFitnessPopulacao = 0
        for cromossomo in populacao:
            somaFitnessPopulacao += Fitness(cromossomo)
        fitnessMedio = somaFitnessPopulacao / len(populacao)
        historicoMelhorFitness.append(novoMelhor)
        historicoFitnessMedio.append(fitnessMedio)
        
        geracao += 1
        novoMelhor = Fitness(ObterMelhorCromossomo(populacao))
        if novoMelhor > velhoMelhor:
             estagnado = 0
        else:
             estagnado += 1
    return ObterMelhorCromossomo(populacao), historicoMelhorFitness, historicoFitnessMedio, geracao 


def Melhores (populacao, n):
    #cria uma lista nova, diferente do sort() que ordena na propria lista, e utiliza o parametro key como critério de ordenação
    populacao_ordenada = sorted(populacao, key=Fitness, reverse=True) 
    escolhidos = populacao_ordenada[:n]
    return escolhidos

def ObterMelhorCromossomo(populacao):
    #pode usar a funcao max() do python que retorna diretamente o maior valor da lista usando menos recursos
    populacao_ordenada = sorted(populacao, key=Fitness, reverse=True)
    return populacao_ordenada[0]

def AgruparEmPares(populacaoSelecionada):
    pares = []

    for i in range(0, len(populacaoSelecionada) - 1, 2):
        pai1 = populacaoSelecionada[i]
        pai2 = populacaoSelecionada[i+1]
        pares.append((pai1, pai2))

    return pares

def Fitness(cromossomo):
    pesoTotal = 0
    valorTotal = 0

    for i in range(len(cromossomo)):
        if cromossomo[i] == 1:
            pesoTotal += PESOS_DOS_ITENS[i]
            valorTotal += VALORES_DOS_ITENS[i]
    
    if pesoTotal > LIMITE_DE_PESO:
        return 0 

    return valorTotal

def CalcularProbabilidades(populacao):
    notas = []
    probabilidades = []

    for cromossomo in populacao:
        notas.append(Fitness(cromossomo))
    somaTotal = sum(notas)

    if somaTotal == 0:
        return [1.0 / len(populacao)] * len(populacao)
    
    for nota in notas:
        probabilidades.append(nota / somaTotal)
    
    return probabilidades

def GirarRoletaUmaVez(populacao, probabilidades):
    i = 0
    soma = probabilidades[i]
    r = random.random()

    while soma < r:
        i += 1
        soma += probabilidades[i]
    
    return populacao[i]

def Roleta(populacao, r):
    probabilidades = CalcularProbabilidades(populacao)
    populacaoSelecionada = []

    for _ in range(r):
        vencedor = GirarRoletaUmaVez(populacao, probabilidades)
        populacaoSelecionada.append(list(vencedor))
    
    return populacaoSelecionada

def Mutacao(alelo):
    if alelo == 1:
        alelo = 0
    else:
        alelo = 1
    return alelo

def Cruzar(pai1, pai2): #crossover// futuramente alterar para usar Slicing (função de python)
    posicao = random.randrange(len(pai1))
    temp = 0
    for i in range(posicao):
        temp = pai1[i]
        pai1[i] = pai2[i]
        pai2[i] = temp

    return pai1, pai2  

def carregar_configuracoes():
    base_dir = Path(__file__).resolve().parent
    pasta_json = base_dir / "json"

    with (pasta_json / "config_sa.json").open(encoding="utf-8") as arquivo:
        configuracoes = json.load(arquivo)

    return configuracoes, pasta_json

def configurar_mochila(config, pasta_json):
    global SEED_EXPERIMENTO
    global LIMITE_DE_PESO
    global TAMANHO_POPULACAO
    global PESOS_DOS_ITENS
    global VALORES_DOS_ITENS

    caminho_itens = pasta_json / config["file"]

    with caminho_itens.open(encoding="utf-8") as arquivo:
        itens = json.load(arquivo)

    PESOS_DOS_ITENS = [item["weight"] for item in itens]
    VALORES_DOS_ITENS = [item["value"] for item in itens]
    SEED_EXPERIMENTO = config["seed"]
    LIMITE_DE_PESO = config["pesoMax"]
    TAMANHO_POPULACAO = config["populacao"]

    random.seed(SEED_EXPERIMENTO)

def main():
    configuracoes, pasta_json = carregar_configuracoes()
    perfis_execucao = ["small", "medium", "big"]

    perfis_faltantes = [perfil for perfil in perfis_execucao if perfil not in configuracoes]
    if perfis_faltantes:
        raise ValueError(
            f"Perfis ausentes em config_sa.json: {', '.join(perfis_faltantes)}."
        )

    historico_melhor_por_perfil = {}
    historico_medio_por_perfil = {}

    for perfil in perfis_execucao:
        configurar_mochila(configuracoes[perfil], pasta_json)

        populacaoInicial = []
        for _ in range(TAMANHO_POPULACAO):
            cromossomo = []
            for _ in range(len(PESOS_DOS_ITENS)):
                cromossomo.append(random.randint(0,1))
            populacaoInicial.append(cromossomo)

        melhorMochila, historicoMelhor, historicoMedio, totalGeracoes = AGCanonico(
            populacaoInicial,
            TAMANHO_POPULACAO,
            TAMANHO_POPULACAO,
            0.8,
            0.05,
        )

        historico_melhor_por_perfil[perfil] = historicoMelhor
        historico_medio_por_perfil[perfil] = historicoMedio

        print(f"[{perfil}] O cromossomo vencedor foi: {melhorMochila} | Valor: {Fitness(melhorMochila)}")
        print(f"[{perfil}] Gerações até a convergência: {totalGeracoes}")

    plt.figure(figsize=(10, 6))
    for perfil in perfis_execucao:
        plt.plot(historico_melhor_por_perfil[perfil], label=perfil)
    plt.title("Melhor Fitness por Geração")
    plt.xlabel("Gerações")
    plt.ylabel("Melhor Fitness")
    plt.legend(title="Mochila")
    plt.grid(True)

    plt.figure(figsize=(10, 6))
    for perfil in perfis_execucao:
        plt.plot(historico_medio_por_perfil[perfil], label=perfil)
    plt.title("Fitness Médio por Geração")
    plt.xlabel("Gerações")
    plt.ylabel("Fitness Médio")
    plt.legend(title="Mochila")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
    