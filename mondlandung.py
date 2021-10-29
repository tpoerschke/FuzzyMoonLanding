import fuzzy
from landing_game import game_tick, game_state, set_lever, uhr

# Fuzzy
m1 = fuzzy.M1(800, 1400) # Geringe Höhe
m2 = fuzzy.M2(900, 2000) # Mittlere Höhe
m3 = fuzzy.M3(1400, 2000) # Große Höhe

# Mengen hier quasi verdreht, wird unten 
# mit "100 - Ausgabe" verrechnet
a1 = fuzzy.M1(12, 65) # Viel Bremskraft
a2 = fuzzy.M2(30, 90) # Mittlere Bremskraft
a3 = fuzzy.M3(60, 70) # Wenig Bremskraft

agg = fuzzy.Aggregator([m1, m2, m3], [a1, a2, a3], 100)
defuzzy = fuzzy.Defuzzy()

# Hauptschleife
while True:
    uhr.tick(30)
    game_tick()
    
    # Aggregieren & Hebel einstellen
    (x, y), _ = agg.aggregate(game_state.hoehe)
    gas_percent = 1 - defuzzy.centroid(x, y) / 100
    set_lever(gas_percent)

    print(f"Gas: {gas_percent*100:.2f}% -> {500 - 200 * gas_percent:.2f}")