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
    pesos = np.random.randint(1, 20, size=n)
    valores = np.random.randint(1, 20, size=n)

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
n = 10
originalValues = mochilaInicial(n)
print(originalValues)
capacity = capacidadeMochila(originalValues)
print(capacidadeMochila(originalValues))


import copy
def solveKnapsackStaticInit():
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
    currentSolution = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    #currentSolution = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]


    currentValue = calculate_value(currentSolution, originalValues, capacity)
    #print(f"Vetor Inicial: {initialSolution}")
    #print(f"Valor Atual: {currentValue}")

    # A melhor solução é a que se tem no momento
    bestSolution = currentSolution[:]
    bestValue = currentValue

    # Temperatura inicial
    # Temperatura recebe um valor "aleatório" que vai dimiuindo conforme aumentar o número e iterações
    temperature = 10000
    #decreaseFactor = 1
    decreaseFactor = 0.9995
    stopTemp = 0.1

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
        #print(valorNeighbor)
        
        if valorNeighbor != 0:    
            
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

    #print(lastAcepted)
    #print(f"Total de iteracoes validas: {totalIteracoes}")
    #print(f"Total de iteracoes invalidas: {igualZero}")
    #print(f"Aceitou o pior: {countPior}")
    #print(f"random: {lastValueRandom}   lastExp: {lastMath}    lastTemp: {lastTemp}")
    #lastSolution = currentValue
    lastSolution = copy.deepcopy(currentSolution)
    return bestSolution, bestValue, lastSolution



def solveKnapsackRandomInit():
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
    currentSolution = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    #currentSolution = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]


    currentValue = calculate_value(currentSolution, originalValues, capacity)
    #print(f"Vetor Inicial: {initialSolution}")
    #print(f"Valor Atual: {currentValue}")

    # A melhor solução é a que se tem no momento
    bestSolution = currentSolution[:]
    bestValue = currentValue

    # Temperatura inicial
    # Temperatura recebe um valor "aleatório" que vai dimiuindo conforme aumentar o número e iterações
    temperature = 10000
    #decreaseFactor = 1
    decreaseFactor = 0.9995
    stopTemp = 0.1

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
        #print(valorNeighbor)
        
        if valorNeighbor != 0:    
            
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

    #print(lastAcepted)
    #print(f"Total de iteracoes validas: {totalIteracoes}")
    #print(f"Total de iteracoes invalidas: {igualZero}")
    #print(f"Aceitou o pior: {countPior}")
    #print(f"random: {lastValueRandom}   lastExp: {lastMath}    lastTemp: {lastTemp}")
    #lastSolution = currentValue
    lastSolution = copy.deepcopy(currentSolution)
    return bestSolution, bestValue, lastSolution


bestSolution, bestValue, lastSolution= solveKnapsackRandomInit()
print(f'Sao iguais? {checkMatriz(bestSolution,lastSolution)}')
print(f'Melhor valor: valor {bestValue}')
totalLast = calculate_value(lastSolution, originalValues, capacity)
print(f'total last value: {totalLast}')
print(f'{lastSolution} Last value')
print(f'{bestSolution} Melhor solução')

import os
import numpy as np
import random
import math
import copy
import matplotlib.pyplot as plt

output_folder = 'SolutionsGraphs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

results = []
last_solution_values = []
num_iterations = 500 

for i in range(num_iterations):
    bestSolution, bestValue, lastSolution = solveKnapsackStaticInit()
    results.append(bestValue)
    total_last_value = calculate_value(lastSolution, originalValues, capacity)
    last_solution_values.append(total_last_value)

# Gráfico 1: Distribuição dos Melhores Valores
unique_values, counts = np.unique(results, return_counts=True)

plt.figure(figsize=(12, 12))

# Gráfico 1: Melhores Valores
plt.subplot(2, 1, 1)  # 2 linhas, 1 coluna, gráfico 1
bars = plt.bar(unique_values, counts, width=1, edgecolor='black', align='center')
plt.xlabel('Valores')
plt.ylabel('Contagem de Execuções')
plt.title(f'Distribuição dos Melhores Valores em {num_iterations} Execuções - Início Estático')
plt.xticks(np.arange(min(unique_values), max(unique_values) + 1, 1))  
plt.grid(axis='y')

# Adicionar linhas pontilhadas nos valores do eixo Y
for i in range(len(counts)):
    plt.axhline(y=counts[i], color='red', linestyle='--', linewidth=0.7) 
    plt.text(unique_values[i], counts[i] + 1, str(counts[i]), ha='center', va='bottom') 

# Gráfico 2: Distribuição dos Valores da Last Solution
unique_last_values, last_counts = np.unique(last_solution_values, return_counts=True)

# Gráfico 2: Last Solution
plt.subplot(2, 1, 2)
bars_last = plt.bar(unique_last_values, last_counts, width=1, edgecolor='black', align='center')
plt.xlabel('Valores da Last Solution')
plt.ylabel('Contagem de Execuções')
plt.title(f'Distribuição dos Valores da Last Solution em {num_iterations} Execuções')
plt.xticks(np.arange(min(unique_last_values), max(unique_last_values) + 1, 1))
plt.grid(axis='y')

# Linhas pontilhadas
for i in range(len(last_counts)):
    plt.axhline(y=last_counts[i], color='red', linestyle='--', linewidth=0.7)
    plt.text(unique_last_values[i], last_counts[i] + 1, str(last_counts[i]), ha='center', va='bottom')

plt.tight_layout()

# Salvar o gráfico na pasta SolutionsGraphs em formato JPG
output_path = os.path.join(output_folder, "Distribuicao_Valores_Init_Static.jpg")
plt.savefig(output_path, format='jpg')

plt.show()


import os
import numpy as np
import random
import math
import copy
import matplotlib.pyplot as plt

# Cria a pasta SolutionsGraphs caso ela não exista
output_folder = 'SolutionsGraphs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

results = []
last_solution_values = []  # Lista para armazenar os valores da lastSolution
num_iterations = 500  # Número de execuções

for i in range(num_iterations):
    bestSolution, bestValue, lastSolution = solveKnapsackRandomInit()
    results.append(bestValue)
    total_last_value = calculate_value(lastSolution, originalValues, capacity)  # Calcula o valor total da lastSolution
    last_solution_values.append(total_last_value)  # Armazena o valor total da lastSolution

# Gráfico 1: Distribuição dos Melhores Valores
unique_values, counts = np.unique(results, return_counts=True)

plt.figure(figsize=(12, 12))

# Gráfico 1: Melhores Valores
plt.subplot(2, 1, 1)  # 2 linhas, 1 coluna, gráfico 1
bars = plt.bar(unique_values, counts, width=1, edgecolor='black', align='center')
plt.xlabel('Valores')
plt.ylabel('Contagem de Execuções')
plt.title(f'Distribuição dos Melhores Valores em {num_iterations} Execuções - Início Randômico')
plt.xticks(np.arange(min(unique_values), max(unique_values) + 1, 1))  # Eixo X de 1 em 1
plt.grid(axis='y')  # Grade para facilitar a visualização

# Adicionar linhas pontilhadas nos valores do eixo Y
for i in range(len(counts)):
    plt.axhline(y=counts[i], color='red', linestyle='--', linewidth=0.7)  # Linha pontilhada
    plt.text(unique_values[i], counts[i] + 1, str(counts[i]), ha='center', va='bottom')  # Adiciona o valor em cima da barra

# Gráfico 2: Distribuição dos Valores da Last Solution
unique_last_values, last_counts = np.unique(last_solution_values, return_counts=True)

# Gráfico 2: Last Solution
plt.subplot(2, 1, 2)  # 2 linhas, 1 coluna, gráfico 2
bars_last = plt.bar(unique_last_values, last_counts, width=1, edgecolor='black', align='center')
plt.xlabel('Valores da Last Solution')
plt.ylabel('Contagem de Execuções')
plt.title(f'Distribuição dos Valores da Last Solution em {num_iterations} Execuções')
plt.xticks(np.arange(min(unique_last_values), max(unique_last_values) + 1, 1))  # Eixo X de 1 em 1
plt.grid(axis='y')  # Grade para facilitar a visualização

# Adicionar linhas pontilhadas nos valores do eixo Y
for i in range(len(last_counts)):
    plt.axhline(y=last_counts[i], color='red', linestyle='--', linewidth=0.7)  # Linha pontilhada
    plt.text(unique_last_values[i], last_counts[i] + 1, str(last_counts[i]), ha='center', va='bottom')  # Valor em cima da barra

# Ajustar layout
plt.tight_layout()

# Salvar o gráfico na pasta SolutionsGraphs em formato JPG
output_path = os.path.join(output_folder, "Distribuicao_Valores_Init_Random.jpg")
plt.savefig(output_path, format='jpg')

plt.show()
