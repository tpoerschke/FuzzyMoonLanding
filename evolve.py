import random, csv, time
from deap import creator, base, tools

import fuzzy
from landing_game import game_state, game_tick, uhr, set_lever, reset_globals

def play(individual):
    input_sets = [
        fuzzy.M1(individual[0], individual[1]),
        fuzzy.M2(individual[2], individual[3]),
        fuzzy.M3(individual[4], individual[5])
    ]

    output_sets = [
        fuzzy.M1(individual[6], individual[7]),
        fuzzy.M2(individual[8], individual[9]),
        fuzzy.M3(individual[10], individual[11])
    ]

    agg = fuzzy.Aggregator(input_sets, output_sets, 100)
    defuzzy = fuzzy.Defuzzy()

    game_state.game_ended = False
    reset_globals()
    while not game_state.game_ended:
        uhr.tick(30)
        game_tick(draw=False)
        # Aggregieren & Hebel einstellen
        (x, y), _ = agg.aggregate(game_state.hoehe)
        try:
            gas_percent = 1 - defuzzy.centroid(x, y) / 100
        except ZeroDivisionError: 
            gas_percent = 1
        set_lever(gas_percent)
        #print(f"Gas: {gas_percent:.2f} | Height: {game_state.hoehe:.2f} | Fuel: {game_state.fuel:.2f}")

def gen_individual():
    mx_list = []
    ax_list = []
    for _ in range(3):
        mx1 = random.randint(0, 1999)
        mx2 = random.randint(mx1+1, 2000)
        mx_list.append(mx1)
        mx_list.append(mx2)
    
        ax1 = random.randint(0, 99)
        ax2 = random.randint(ax1+1, 100)
        ax_list.append(ax1)
        ax_list.append(ax2)
    ind = creator.Individual()
    ind.extend([*mx_list, *ax_list])
    return ind

def evaluate(individual):
    play(individual)
    if game_state.success:
        return abs(game_state.velocity),
    else:
        return abs(game_state.velocity) * 1000,


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", gen_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=[2000]*6 + [100]*6, indpb=0.05) # TODO: gewährleisten, dass x1 < x2 gilt
toolbox.register("select", tools.selTournament, tournsize=3)


pop = toolbox.population(n=100)
# Population evaluieren
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

# CXPB:  Wahrscheinlichkeit, dass sich zwei Individuen paaren
# MUTPB: Wahrscheinlichkeit, dass ein Individuum mutiert
CXPB, MUTPB = 0.5, 0.2

# Fitness-Werte extrahieren
fits = [ind.fitness.values[0] for ind in pop]

gen = 0
# Lasset die Evolution beginnen
# Ab 15m/s gilt eine Landung als erfolgreich, 
# daher wird dann abgebrochen. Kann verringert
# werden, wenn eine sanftere Landung 
# erforderlich ist. Auch gamestate.success könnte
# Anwendung finden, dann kann jedoch nicht die
# Geschwindigkeit kontrolliert werden. 
while min(fits) > 15 and gen < 1000:
    # A new generation
    gen += 1
    print(f"-- Generation {gen} --")
    # Nächste Generation auswählen
    offspring = toolbox.select(pop, len(pop))
    # Klonen zur Manipulation
    offspring = list(map(toolbox.clone, offspring))
    # Crossover
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    # Mutation
    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    # Manipulierte Individuen erneut evaluieren
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    # Poulation ersetzen
    pop[:] = offspring
    # Fitness-Werte extrahieren
    fits = [ind.fitness.values[0] for ind in pop]
    # Statistiken
    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x*x for x in fits)
    std = abs(sum2 / length - mean**2)**0.5
    print("  Num %s" % length)
    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))
    print("  Avg %s" % mean)
    print("  Std %s" % std)

# Individuuen der letzten Generation speichern
with open(f'individuals_{time.time():.0f}.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for ind, fit in zip(pop, fits):
        writer.writerow([fit] + list(ind))