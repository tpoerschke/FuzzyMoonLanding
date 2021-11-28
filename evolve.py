import os, random, csv, time, multiprocessing, argparse
from deap import creator, base, tools

import fuzzy
from landing_game import LandingGame

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

    lg = LandingGame()
    lg.game_state.game_ended = False
    while not lg.game_state.game_ended:
        lg.uhr.tick(30)
        lg.game_tick(draw=False)
        # Aggregieren & Hebel einstellen
        (x, y), _ = agg.aggregate(lg.game_state.hoehe)
        try:
            gas_percent = 1 - defuzzy.centroid(x, y) / 100
        except ZeroDivisionError: 
            gas_percent = 1
        lg.set_lever(gas_percent)
        #print(f"Gas: {gas_percent:.2f} | Height: {game_state.hoehe:.2f} | Fuel: {game_state.fuel:.2f}")
    return lg.game_state

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
    game_state = play(individual)
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

def main(args):
    N_PROCESSES = 20
    pool = multiprocessing.Pool(N_PROCESSES)
    print(f"Anzahl an Prozessen: {N_PROCESSES}")
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=args.pop)
    # Population evaluieren
    print(f"-- Generation Genesis --")
    t0 = time.perf_counter()
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    t = int(time.perf_counter() - t0)
    print(f"evaluated in {t} secs...")

    # CXPB:  Wahrscheinlichkeit, dass sich zwei Individuen paaren
    # MUTPB: Wahrscheinlichkeit, dass ein Individuum mutiert
    CXPB, MUTPB = 0.5, 0.2

    # Fitness-Werte extrahieren
    fits = [ind.fitness.values[0] for ind in pop]

    gen = 0
    pop_hist, mean_hist, max_hist, min_hist, time_hist = [], [], [], [], []
    # Lasset die Evolution beginnen
    # Ab 15m/s gilt eine Landung als erfolgreich, 
    # daher wird dann abgebrochen. Kann verringert
    # werden, wenn eine sanftere Landung 
    # erforderlich ist. Auch gamestate.success könnte
    # Anwendung finden, dann kann jedoch nicht die
    # Geschwindigkeit kontrolliert werden. 
    while min(fits) > args.target_fitness and gen < args.max_gen:
        t0 = time.perf_counter()
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
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # Poulation ersetzen
        pop[:] = offspring
        # Fitness-Werte extrahieren
        fits = [ind.fitness.values[0] for ind in pop]
        # Statistiken
        length = len(pop)
        mean = sum(fits) / length
        min_ = min(fits)
        max_ = max(fits)
        t = int(time.perf_counter() - t0)
        print("  Pop %s" % length)
        print("  Min %s" % min_)
        print("  Max %s" % max_)
        print("  Avg %s" % mean)
        print("  T   %s" % t)
        pop_hist.append(length)
        mean_hist.append(mean)
        min_hist.append(min_)
        max_hist.append(max_)
        time_hist.append(t)

    # Individuuen der letzten Generation speichern
    timestamp = time.time()
    with open(f'individuals_{timestamp:.0f}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for ind, fit in zip(pop, fits):
            writer.writerow([fit] + list(ind))
    # Informationen zum Durchlauf speichern
    with open(f'stats_{timestamp:.0f}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["pop", "mean", "max", "min", "t"])
        for pop, mean, max_, min_, t in zip(pop_hist, mean_hist, max_hist, min_hist, time_hist):
            writer.writerow([pop, mean, max_, min_, t])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--target-fitness', type=int, required=False, default=10, help="Fitness, die erreicht werden soll.")
    parser.add_argument('--pop', type=int, required=False, default=50, help="Größe der Population.")
    parser.add_argument('--max-gen', type=int, required=False, default=100, help="Maximale Anzahl an Generationen.")
    args = parser.parse_args()
    main(args)