MAX_GERACOES = 10
def AGCanonico(populacao, n, r, pCross, pMut):
    '''
    n = quantidade da populacao (r = n normalmente)
    r = quantidade dos descendentes (r = n normalmente)
    pCross = probabilidade de crossover (0.8 tipico)
    pMut = probabilidade de mutacao (0.05 tipico)
    '''
    while(geracao < MAX_GERACOES): # and (objetivo nao foi alcancado) and (melhor fitness nao esta estagnado)
        objetivo = []
        for c in populacao:
            Fitness(c)
        geracao = 0
        populacaoSelecionada = Roleta(r)
        descendentesCruzados = []
        for pai1,pai2 in populacaoSelecionada:
            if (Random(0,1) < pCross): # numeros decimais entre 0 e 1, decidir com quantas casas decimais
                filho1, filho2 = Cruzar(pai1, pai2) # descobrir qual vetor guarda as infos de pai e filho
            else: 
                filho1, filho2 = pai1, pai2
            descendentesCruzados.append(filho1, filho2)
        descendentesMutados = []
        for c in descendentesCruzados:
            for alelo(gene) in c: # entender melhor essa parte de alelo e gene
                if(Random(0,1) < pMut):
                    pass # ToDo altera o valor do alelo
            descendentesMutados.append(c)
        for c in descendentesMutados:
            Fitness(c)
        populacaoTotal = Unir(populacao, descendentesMutados)    
        populacao = melhores(c) # entender como armazenar os melhores
        geracao = geracao + 1
    
    return c 
    

def Fitness(c):
    pass

def Roleta(r):
    pass

def Cruzar(i, j):
    pass