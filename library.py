import fuzzy

SETS3 = "3 sets"
SETS3_EA1 = "3 sets ea 1"
SETS5_STANDARD = "5 sets"
SETS5_SMOOTH = "5 sets smooth"
ALL_VARIANTS = (SETS3, SETS3_EA1, SETS5_STANDARD, SETS5_SMOOTH)

# Standard (3 Sets)
def _sets31():
    m1 = fuzzy.M1(800, 1400) # Geringe Höhe
    m2 = fuzzy.M2(900, 2000) # Mittlere Höhe
    m3 = fuzzy.M3(1400, 2000) # Große Höhe
    input_sets = (m1, m2, m3)
    # Mengen hier quasi verdreht, wird 
    # mit "100 - Ausgabe" verrechnet
    a1 = fuzzy.M1(12, 65) # Viel Bremskraft
    a2 = fuzzy.M2(30, 90) # Mittlere Bremskraft
    a3 = fuzzy.M3(60, 70) # Wenig Bremskraft
    output_sets = (a1, a2, a3)
    return input_sets, output_sets

# EA
def _sets32ea1():
    m1 = fuzzy.M1(1983, 1808) 
    m2 = fuzzy.M2(1436, 1867)
    m3 = fuzzy.M3(292, 1427)
    input_sets = (m1, m2, m3)
    a1 = fuzzy.M1(43, 68)
    a2 = fuzzy.M2(25, 66)
    a3 = fuzzy.M3(28, 71)
    output_sets = (a1, a2, a3)
    return input_sets, output_sets

# Standard (5 Sets)
def _sets51():
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
    return input_sets, output_sets

# Bremskraft wird am Ende verringert (5 Sets)
def _sets52():
    m1 = fuzzy.M1(50, 500)    # Sehr geringe Höhe
    m2 = fuzzy.M2(400, 1200)  # Geringe Höhe
    m3 = fuzzy.M2(900, 1600)  # Mittlere Höhe
    m4 = fuzzy.M2(1200, 2000) # Große Höhe
    m5 = fuzzy.M3(1400, 2000) # Sehr große Höhe
    input_sets = (m1, m2, m3, m4, m5)
    a1 = fuzzy.M2(20, 50) # Weniger Bremskraft
    a2 = fuzzy.M1(20, 40) # Viel Bremskraft
    a3 = fuzzy.M2(30, 60) # Mittlere Bremskraft
    a4 = fuzzy.M2(40, 70) # Wenig Bremskraft
    a5 = fuzzy.M3(60, 75) # Sehr Wenig Bremskraft
    output_sets = (a1, a2, a3, a4, a5)
    return input_sets, output_sets


def load_sets(sets_type):
    return {
        SETS3: _sets31(),
        SETS3_EA1: _sets32ea1(),
        SETS5_STANDARD: _sets51(),
        SETS5_SMOOTH: _sets52()
    }.get(sets_type, SETS3)