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

import numpy as np

def mochilaInicial(n):
    # Gerando valores aleatórios para pesos e valores dos itens
    pesos = np.random.randint(0, 16, size=n)
    valores = np.random.randint(0, 16, size=n)

    # Construindo a matriz com pesos e valores
    matriz = np.array([pesos, valores])

    return matriz

def capacidadeMochila(matriz):
    somaTotal = np.sum(matriz[0])
    percentage = 0.35
    capacidade = int(somaTotal * percentage)
    return capacidade

def checkMatriz(matriz1, matriz2):
    # Verifica se as duas matrizes são exatamente iguais
    return np.array_equal(matriz1, matriz2)

# Fornecer uma opção randomica de itens que estariam inseridos nessa primeira lista de solução
def initRandom(size):
    # 100% random! 
    randomVector = np.random.choice([0, 1], size=size)
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
                return 0
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


#Quantidade de Itens 
n = 24
originalValues = mochilaInicial(n)
print(originalValues)
capacity = capacidadeMochila(originalValues)
print(capacidadeMochila(originalValues))


import copy
def solveKnapsack():
    # Perguntar a capacidade total da Mochila
    # capacity = int(input("Bag Capacity: "))
    #capacity = 20


    # Comecar perguntando sobre os items
    #originalValues = askForItens()
    #originalValues = np.array([
    #[2, 3, 4, 5, 9, 7, 1, 6, 4, 8, 3, 5],  # Pesos
    #[3, 4, 5, 8, 10, 7, 2, 9, 6, 12, 5, 7]  # Valores
    #[12, 7, 11, 8, 9, 15, 6, 4, 13, 8, 12, 9, 7, 5, 11, 6, 10, 4, 9, 7],
    #[24, 13, 23, 15, 16, 30, 10, 8, 25, 20, 24, 17, 14, 12, 23, 9, 21, 7, 19, 13]
    #])

    # Definir estados Iniciais - Aleatório
    #currentSolution = initRandom(originalValues.shape[1])
    currentSolution = [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]

    currentValue = calculate_value(currentSolution, originalValues, capacity)
    #print(f"Vetor Inicial: {initialSolution}")
    #print(f"Valor Atual: {currentValue}")

    # A melhor solução é a que se tem no momento
    bestSolution = currentSolution [:]
    bestValue = currentValue

    # Temperatura inicial
    # Temperatura recebe um valor "aleatório" que vai dimiuindo conforme aumentar o número e iterações
    temperature = 1000
    #decreaseFactor = 1
    decreaseFactor = 0.9
    stopTemp = 5

    # Stuck count para "sair" de loops ruins
    # NAO ALTERAR A TEMPERATURA MANUALMENTE!
    stuckCount = 0
    maxStuckCount = 1000

    igualZero = 0 
    totalIteracoes = 0
    countPior = 0
    lastAcepted = 0
    lastValueRandom = 0
    lastMath = 0  
    lastTemp = 0

    # Loop infinito - O critério de parada é se não vai aceitar mais variações ("Temperatura"<=0)
    # Loop infinito - O critério de parada é se não vai aceitar mais variações ("Temperatura"<=0)
    while temperature > stopTemp:
        # Ver Neighbor
        Neighbor = RandomNeighbor(currentSolution)
        valorNeighbor = calculate_value(Neighbor, originalValues, capacity)
        
        if valorNeighbor != 0:    
            lastSolution = copy.deepcopy(currentSolution)
            # Fit = Próximo - Atual > para ver se é melhor que a atual
            fitness = valorNeighbor - currentValue
            totalIteracoes= totalIteracoes + 1
            # Se Valor Neighbor for MAIOR que o valor ATUAL
            if fitness > 0:
                # Se for MAIOR: Atual = Próximo
                currentSolution = copy.deepcopy(Neighbor)
                currentValue = valorNeighbor
                lastAcepted = 1
            # Se NÃO for MAIOR
            else:
                # Se existe a probabilidade de aceitar
                lastValueRandom = random.uniform(0, 1)
                lastMath = math.exp(fitness / temperature)
                if lastValueRandom < lastMath:
                    # Então Atual = Próximo
                    countPior = countPior + 1
                    currentSolution = copy.deepcopy(Neighbor)
                    currentValue = valorNeighbor
                    lastAcepted = 2
            
            # Guarda o maior
            if currentValue > bestValue:
                bestValue = currentValue
                bestSolution = copy.deepcopy(currentSolution)

            temperature = temperature * decreaseFactor
            #temperature = temperature - decreaseFactor
            lastTemp = temperature
        else:
            igualZero = igualZero + 1

    print(lastAcepted)
    #print(f"Total de iteracoes validas: {totalIteracoes}")
    #print(f"Total de iteracoes invalidas: {igualZero}")
    #print(f"Aceitou o pior: {countPior}")
    print(f"random: {lastValueRandom}   lastExp: {lastMath}    lastTemp: {lastTemp}")
    return bestSolution, bestValue, lastSolution, lastTemp


bestSolution, bestValue, lastSolution, lastTemp= solveKnapsack()
print(f'Sao iguais? {checkMatriz(bestSolution,lastSolution)}')
print(f'Melhor valor: valor {bestValue}')
totalLast = calculate_value(lastSolution, originalValues, capacity)
print(f'total last value: {totalLast}')
print(f'{lastSolution} Last value')
print(f'{bestSolution} Melhor solução')
print(f'{lastTemp:.2f} Ultima temp')