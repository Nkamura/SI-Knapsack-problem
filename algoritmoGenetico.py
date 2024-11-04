import random
import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
n = 14
n_geracoes = 100
tam_populacao = 50
taxa_mutacao = 0.1

# Função para inicializar os valores e pesos dos itens na mochila
def mochila_inicial(n):
    # Gerando valores aleatórios para pesos e valores dos itens
    pesos = np.random.randint(1, 16, size=n)
    valores = np.random.randint(1, 16, size=n)
    # Construindo a matriz com pesos e valores
    matriz = np.array([pesos, valores])
    return matriz

# Função para definir a capacidade da mochila com base em uma porcentagem do peso total
def capacidade_mochila(matriz):
    somaTotal = np.sum(matriz[0])
    percentage = 0.35
    capacidade = int(somaTotal * percentage)
    return capacidade

def avaliar_fitness(individuo, matriz, capacidade):
    peso_total = np.sum(individuo * matriz[0])
    valor_total = np.sum(individuo * matriz[1])
    if peso_total > capacidade:
        return 0  
    return valor_total

# Seleção por roleta
def selecao_por_roleta(populacao, fitness):
    soma_fitness = np.sum(fitness)
    probabilidades = [aptidao / soma_fitness for aptidao in fitness]
    pai1_idx = np.random.choice(len(populacao), p=probabilidades)
    soma_fitness = soma_fitness - fitness[pai1_idx]
    for aptidao in range(len(fitness)):
        if aptidao == pai1_idx:
            probabilidades[aptidao] = 0
        else:
            if(fitness[aptidao] == 0):
                probabilidades[aptidao] = 0
            else:
                print(fitness[aptidao], 'fitness')
                print(fitness[aptidao] / soma_fitness)
                probabilidades[aptidao] = fitness[aptidao] / soma_fitness
    if(np.sum(probabilidades) == 0):
        probabilidades = [1/len(probabilidades) for i in probabilidades]
    pai2_idx = np.random.choice(len(populacao), p=probabilidades)
    
    return populacao[pai1_idx],populacao[pai2_idx]

# Função de cruzamento
def cruzamento(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = np.concatenate((pai1[:ponto], pai2[ponto:]))
    filho2 = np.concatenate((pai2[:ponto], pai1[ponto:]))

    return filho1, filho2

# Função de mutação
def mutacao(individuo, taxa_mutacao=0.1):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]  
    return individuo

# Função para calcular o melhor indivíduo
def calcula_melhor_individuo(populacao, matriz, capacidade):
    melhor_valor = 0
    melhor_individuo = None
    for individuo in populacao:
        peso_total = np.sum(individuo * matriz[0])
        valor_total = np.sum(individuo * matriz[1])
        if peso_total <= capacidade and valor_total > melhor_valor:
            melhor_valor = valor_total
            melhor_individuo = individuo
    return melhor_individuo

# Função principal do algoritmo genético
def algoritmo_genetico(matriz, capacidade, n_geracoes=100, tam_populacao=50, taxa_mutacao=0.1):
    populacao = np.random.randint(0, 2, (tam_populacao, matriz.shape[1]))
    historico_fitness = []

    for _ in range(n_geracoes):
        fitness = [avaliar_fitness(ind, matriz, capacidade) for ind in populacao]
        nova_populacao = []

        while len(nova_populacao) < tam_populacao:
            pai1,pai2 = selecao_por_roleta(populacao, fitness)
            filho1, filho2 = cruzamento(pai1, pai2)
            nova_populacao.extend([mutacao(filho1, taxa_mutacao), mutacao(filho2, taxa_mutacao)])
        populacao = np.array(nova_populacao[:tam_populacao])
        historico_fitness.append(max(fitness))

    melhor_fitness = max(fitness)
    melhor_individuo = calcula_melhor_individuo(populacao, matriz, capacidade)

    return melhor_individuo, melhor_fitness, historico_fitness, fitness

# Execução do algoritmo genético
matriz = mochila_inicial(n)
capacidade = capacidade_mochila(matriz)
melhor_individuo, melhor_fitness, historico_fitness, fitness_ultima_geracao = algoritmo_genetico(
    matriz, capacidade, n_geracoes, tam_populacao, taxa_mutacao
)

# Exibindo resultados
print("Melhor combinação de itens da última geração:", melhor_individuo)
print("Valor máximo encontrado:", melhor_fitness)
peso_total = np.sum(melhor_individuo * matriz[0])
valor_total = np.sum(melhor_individuo * matriz[1])
print("Peso total do melhor valor da última geração:", peso_total)
print("Valor total do melhor valor da última geração:", valor_total)

plt.figure(figsize=(12, 6))
plt.plot(historico_fitness, label="Melhor valor fitness ao longo das gerações")
plt.xlabel("Gerações")
plt.ylabel("Valor Fitness")
plt.title("Evolução do Melhor Valor Fitness ao Longo das Gerações")
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(fitness_ultima_geracao, 'o', label="Valores fitness da última geração")
plt.xlabel("Indivíduos")
plt.ylabel("Valor Fitness")
plt.title("Valores Fitness dos Indivíduos na Última Geração")
plt.legend()
plt.show()
