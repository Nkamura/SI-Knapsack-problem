import numpy as np

# Function created to initialize the Item vector - implement one that gets the data from a .txt file
# https://awari.com.br/vetor-python-aprenda-a-utilizar-a-linguagem-de-programacao-para-manipular-vetores/
def askForItens():
    qntd_itens = int(input("Type the number of items:"))
    #Create maze with dimension 2xItems    
    matriz = np.zeros((2, qntd_itens))
    
    ## Fill Valor
    for i in range(qntd_itens):
        matriz[0][i] = int(input(f"Type the Value for each item {i+1}:"))
    ## Fill Peso
    for i in range(qntd_itens):
        matriz[1, i] = float(input(f"Type the Weight for each item {i+1}: "))
    return matriz


# Fornecer uma opção randomica de itens que estariam inseridos nessa primeira lista de solução
def initRandom(size):
    # 100% random! 
    randomVector = np.random.choice([True, False], size=size)
    return randomVector


import random
import math

# Calcular o valor total a mochila com os itens dentro dela
def calculate_value(solution, original, capacity):
    total_weight = 0
    total_value = 0

    # Loop para percorrer o vetor inteiro
    for i in range(len(solution)):
        # Calcular o peso e valor total para cada item que estiver presente 
        if(solution[i] == 1):
            # Coluna o item que foi selecionado
            total_weight += original[0][i]
            total_value += original[1][i]
            # Desconsidera se tiver ultrapassado a capacidade
            if(total_weight > capacity):
                # Retorna um valor negativo para indicar que estourou
                return -1
    return total_value


def RandomNeighbor(solution):
    # [:] é utilizado para criar uma cópia sem referenciar o mesmo espaço de memória
    # já que, se for apontando os 2 para o mesmo lugar, se eu alterar altera ambos - PARA VETORES
    tempSolution = solution[:]
    # Ver quais itens estarão na mochila - pelo índice 
    index = random.randint(0, len(solution) - 1)
    # 1 - 0 = 1  e  1 - 1 = 0
    tempSolution[index] = 1 - tempSolution[index]  # inverte o valor de 0 para 1 ou de 1 para 0
    return tempSolution


import copy
def solveKnapsack():
    # Perguntar a capacidade total da Mochila
    # capacity = int(input("Bag Capacity: "))
    capacity = 20

    # Comecar perguntando sobre os items
    #originalValues = askForItens()
    originalValues = np.array([
    [2, 3, 4, 5, 9, 7, 1, 6, 4, 8, 3, 5],  # Pesos
    [3, 4, 5, 8, 10, 7, 2, 9, 6, 12, 5, 7]  # Valores
])

    # Definir estados Iniciais - Aleatório
    currentSolution = initRandom(originalValues.shape[1])
    currentValue = calculate_value(currentSolution, originalValues, capacity)
    #print(f"Vetor Inicial: {initialSolution}")
    #print(f"Valor Atual: {currentValue}")

    # A melhor solução é a que se tem no momento
    bestSolution = currentSolution [:]
    bestValue = currentValue

    # Temperatura inicial
    # Temperatura recebe um valor "aleatório" que vai dimiuindo conforme aumentar o número e iterações
    temperature = 10000
    decreaseFactor = 0.95
    stopTemp = 10

    # Stuck count para "sair" de loops ruins
    stuckCount = 0
    maxStuckCount = 1000

    # Loop infinito - O critério de parada é se não vai aceitar mais variações ("Temperatura"<=0)
    # Loop infinito - O critério de parada é se não vai aceitar mais variações ("Temperatura"<=0)
    while temperature > stopTemp:
        # Ver Neighbor
        Neighbor = RandomNeighbor(currentSolution)
        valorNeighbor = calculate_value(Neighbor, originalValues, capacity)
        
        # Fit = Próximo - Atual > para ver se é melhor que a atual
        fitness = valorNeighbor - currentValue
        
        # Se Valor Neighbor for MAIOR que o valor ATUAL
        if fitness > 0:
            # Se for MAIOR: Atual = Próximo
            currentSolution = copy.deepcopy(Neighbor)
            currentValue = valorNeighbor
        # Se NÃO for MAIOR
        else:
            # Se existe a probabilidade de aceitar
            if random.uniform(0, 1) < math.exp(fitness / temperature):
                # Então Atual = Próximo
                currentSolution = copy.deepcopy(Neighbor)
                currentValue = valorNeighbor
        
        # Guarda o maior
        if currentValue > bestValue:
            bestValue = currentValue
            bestSolution = copy.deepcopy(currentSolution)

        temperature *= decreaseFactor

    return bestSolution, bestValue



bestSolution, bestValue = solveKnapsack()
print(f'Melhor solução: {bestSolution} com valor {bestValue}')