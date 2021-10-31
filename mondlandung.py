import argparse

import fuzzy
from landing_game import game_tick, game_state, set_lever, uhr
from plotting import Plotting

parser = argparse.ArgumentParser()
parser.add_argument('--n-sets', type=int, required=False, default=3, choices=[3, 5])
parser.add_argument('--live-plot', action='store_const', const=True, required=False)
parser.add_argument('--debug', action='store_const', const=True, required=False)
args = parser.parse_args()


m1 = fuzzy.M1(800, 1400) # Geringe Höhe
m2 = fuzzy.M2(900, 2000) # Mittlere Höhe
m3 = fuzzy.M3(1400, 2000) # Große Höhe
input_sets = (m1, m2, m3)

# Mengen hier quasi verdreht, wird unten 
# mit "100 - Ausgabe" verrechnet
a1 = fuzzy.M1(12, 65) # Viel Bremskraft
a2 = fuzzy.M2(30, 90) # Mittlere Bremskraft
a3 = fuzzy.M3(60, 70) # Wenig Bremskraft
output_sets = (a1, a2, a3)

if args.n_sets == 5:
    m1 = fuzzy.M1(100, 900)   # Sehr geringe Höhe
    m2 = fuzzy.M2(400, 1200)  # Geringe Höhe
    m3 = fuzzy.M2(900, 1600)  # Mittlere Höhe
    m4 = fuzzy.M2(1200, 2000) # Große Höhe
    m5 = fuzzy.M3(1400, 2000) # Sehr große Höhe
    input_sets = (m1, m2, m3, m4, m5)

    a1 = fuzzy.M1(26, 30) # Sehr Viel Bremskraft
    a2 = fuzzy.M2(26, 50) # Viel Bremskraft
    a3 = fuzzy.M2(30, 60) # Mittlere Bremskraft
    a4 = fuzzy.M2(40, 70) # Wenig Bremskraft
    a5 = fuzzy.M3(60, 75) # Sehr Wenig Bremskraft
    output_sets = (a1, a2, a3, a4, a5)

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