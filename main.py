import random
import matplotlib.pyplot as plt

#SEED_EXPERIMENTO = 104
MAX_GERACOES = 100
PESOS_DOS_ITENS = [12, 7, 11, 8, 9, 6, 7, 3, 5, 9]
VALORES_DOS_ITENS = [24,13, 23,15,16,12,13, 7, 9,17]
LIMITE_DE_PESO = 35

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
    #estagnado = 0


    historicoMelhorFitness = []
    historicoFitnessMedio = []

    while geracao < MAX_GERACOES: #and estagnado != 15:
        populacaoSelecionada = Roleta(populacao, r)
        descendentesCruzados = []
        #velhoMelhor = Fitness(ObterMelhorCromossomo(populacao))

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
        
        for cromossomo in descendentesMutados:
            Fitness(cromossomo)

        # Reposicao geracional: a nova geracao e formada apenas pelos descendentes.
        populacao = descendentesMutados[:n]

        novoMelhor = Fitness(ObterMelhorCromossomo(populacao))
        
        somaFitnessPopulacao = 0
        for cromossomo in populacao:
            somaFitnessPopulacao += Fitness(cromossomo)
        fitnessMedio = somaFitnessPopulacao / len(populacao)
        historicoMelhorFitness.append(novoMelhor)
        historicoFitnessMedio.append(fitnessMedio)
        
        geracao += 1
        # novoMelhor = Fitness(ObterMelhorCromossomo(populacao))
        # if novoMelhor > velhoMelhor:
        #     estagnado = 0
        # else:
        #     estagnado += 1
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


def main():
    #random.seed(SEED_EXPERIMENTO)

    populacaoInicial = []
    for _ in range(50):
        cromossomo = []
        for _ in range(len(PESOS_DOS_ITENS)):
            cromossomo.append(random.randint(0,1))
        populacaoInicial.append(cromossomo)

    melhorMochila, historicoMelhor, historicoMedio, totalGeracoes = AGCanonico(populacaoInicial, 50, 50, 0.8, 0.05)
    print(f"O cromossomo vencedor foi: {melhorMochila} | Valor: {Fitness(melhorMochila)}")
    print(f"Gerações até a convergência: {totalGeracoes}")

    plt.figure(figsize=(10, 6))
    plt.plot(historicoMelhor, label='Melhor Fitness', color='green', linewidth=2)
    plt.plot(historicoMedio, label='Fitness Médio', color='orange', linestyle='--')

    plt.title('Evolução do Algoritmo Genético - Problema da Mochila')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.legend() 
    plt.grid(True)

    plt.show()

main()
    