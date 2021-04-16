# Imports necessários
import random
from deap import creator, base, tools, algorithms

# Definindo peso máximo da mochila - Caso necessário, altere o valor do peso para gerações diferentes
PESO_MÁXIMO = 20

#Criando itens
def criar_itens(qtd_itens):
    itens = []
    for x in range(qtd_itens):
        itens.append({"peso": random.randint(1,10), "valor": random.uniform(1, 100)})
    return itens

# Adicionando os itens criados a uma lista
itens = criar_itens(10)

# Define o tipo fitness: Um objetivo com maximização
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Define o tipo indivíduo: indivíduo do tipo list (array) com
# a fitness definida anteriormente.
creator.create("Individual", list, fitness=creator.FitnessMax)

# Toolbox para inicialização de componentes do algoritmo
toolbox = base.Toolbox()

# Atributo booleano criado de forma aleatório
toolbox.register("attr_bool",
                 random.random)

# Indivíduo (tipo Inidividual) criado a partir do atributo definido
# anteriormente. Ou seja, indivíduo do tipo booleano.
# São criados 10 indivíduos. initRepeat faz esse papel
toolbox.register("individual",
                 tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)

# Criação da população, do tipo lista composto
# por indivíduos (individual)
toolbox.register("population",
                 tools.initRepeat, list, toolbox.individual)

# Criação da função de fitness.
# A função recebe um indivíduo e retorna uma tupla
# que representa a avaliação do indivíduo
def evalOneMax(individual):
    valor = 0
    peso = 0
    for index in range(len(individual)):
        if individual[index] > 0.5:
            valor += itens[index]['valor']
            peso += itens[index]['peso']
    if (peso > PESO_MÁXIMO):
        return 100000000, 0
    return peso, valor
 
#Função para obter os itens 
def obter_itens(individual):
    itens_obtencao = []
    for index in range(len(individual)):
        if individual[index] > 0.5:
            itens_obtencao.append((index, itens[index]))
    return itens_obtencao

# registra a função de fitness
toolbox.register("evaluate", evalOneMax)

# registro dos operadores
toolbox.register("mate", tools.cxTwoPoint)  # crossover
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)  # mutação

# registro do método de seleção
toolbox.register("select", tools.selTournament, tournsize=3)

# tamanho da população
population = toolbox.population(n=300)

# iniciando o processo de evolução
# número de gerações

NGEN = 50
for gen in range(NGEN):

    # O módulo algorithms implementa vários algoritmos evolucionários
    # Na documentação tem a lista:
    # https://deap.readthedocs.io/en/master/api/algo.html
    # varAnd aplica operações de mutação e crossover
    # cxpb: probabilidade de crossover
    # mutpb: probabilidade de mutação
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    # avalia cada indivíduo
    fits = toolbox.map(toolbox.evaluate, offspring)

    # associa cada indivíduo ao seu valor de fitness
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = [fit[1]]

    # aplica a seleção para gerar a nova população
    population = toolbox.select(offspring, k=len(population))

# retorna o k melhor indivíduos da última população
top10 = tools.selBest(population, k=5)

# Obtém a lista de itens selecionados
itens = obter_itens(top10[0])

# Faz o mapeamento para obtenção dos valores de peso e valor
pesos = list(map(lambda x: x[1]['peso'], itens))
valores = list(map(lambda x: x[1]['valor'], itens))

# Imprime o peso e o valor total da mochila
print("O peso máximo da mochila é ", PESO_MÁXIMO)
print("Peso Ideal: {0} | Valor Ideal: {1:.2f} ".format(sum(pesos), sum(valores)))