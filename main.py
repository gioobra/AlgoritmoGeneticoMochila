import random

MAX_GERACOES = 10
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

    while geracao < MAX_GERACOES and not Objetivo() and not MelhorFitnessEstagnado():
        populacaoSelecionada = Roleta(populacao, r)
        descendentesCruzados = []
        for pai1,pai2 in AgruparEmPares(populacaoSelecionada):
            if (random.random() < pCross): # decide entre 0.0 e 1.0
                filho1, filho2 = Cruzar(pai1, pai2) 
            else: 
                filho1, filho2 = pai1, pai2
            descendentesCruzados.append(filho1, filho2)
        
        descendentesMutados = []
        for cromossomo in descendentesCruzados:
            for alelo in cromossomo:
                if(random.random() < pMut):
                    Mutacao(alelo)
            descendentesMutados.append(cromossomo)
        
        for cromossomo in descendentesMutados:
            Fitness(cromossomo)
        populacaoTotal = populacao + descendentesMutados   
        populacao = Melhores(populacao, n) 
        geracao += 1
    
    return ObterMelhorCromossomo(populacao) 


def Melhores (populacao, n):
    pass

def ObterMelhorCromossomo(populacao):
    pass

def AgruparEmPares():
    pass

def MelhorFitnessEstagnado():
    pass    

def Fitness(c):
    peso = c[0]*1 + c[1]*2 #conta do peso da mochila, considerando que tudo dentro do vetor eh 0 ou 1
    if peso <= 10: 
        for i in c:
            itens = itens + c[i]
    #se o peso eh sempre menor ou igual o estipulado, o que pode variar mais eh o numero de itens, sendo assim a melhor mochila eh a que carrega o maior valor de peso com mais itens        
    return peso + itens

def Roleta(r):
    pass

def Mutacao(alelo):
    pass

def Cruzar(i, j):
    pass

def Objetivo():
    x = 10 # max valor possivel da melhor mochila
    y = 10 # max de itens possiveis da melhor mochila
    peso = c[0]*1 + c[1]*2 #conta do peso da mochila, considerando que tudo dentro do vetor eh 0 ou 1
    for i in c:
        itens = itens + c[i]
    if peso == x and itens == y:
        return 1
    else:
        return 0
    