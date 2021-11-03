import argparse

import fuzzy, library
from landing_game import game_tick, game_state, set_lever, uhr
from plotting import Plotting

parser = argparse.ArgumentParser()
parser.add_argument('--variant', type=str, required=False, default=library.SETS3, choices=library.ALL_VARIANTS, help="Verwendet die gewählte Konfiguration an Fuzzy-Mengen.")
parser.add_argument('--live-plot', action='store_const', const=True, required=False, help="Zeigt eine Visualisierung während die Rakete landet. (Sehr unperformant!)")
parser.add_argument('--debug', action='store_const', const=True, required=False)
args = parser.parse_args()

input_sets, output_sets = library.load_sets(args.variant)

agg = fuzzy.Aggregator(input_sets, output_sets, 100)
defuzzy = fuzzy.Defuzzy()

plotting = None
if args.live_plot:
    plotting = Plotting(input_sets, output_sets, agg, defuzzy)
# Hauptschleife
while True:
    uhr.tick(30)
    game_tick()
    
    # Aggregieren & Hebel einstellen
    (x, y), _ = agg.aggregate(game_state.hoehe)
    gas_percent = 1 - defuzzy.centroid(x, y) / 100
    set_lever(gas_percent)

    if plotting:
        plotting.update(game_state.hoehe)
    if args.debug:
        print(f"Gas: {gas_percent*100:.2f}% -> {500 - 200 * gas_percent:.2f}")