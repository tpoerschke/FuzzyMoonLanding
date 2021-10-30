import time
import matplotlib.pyplot as plt

import fuzzy

m1 = fuzzy.M1(800, 1400) # Geringe Höhe
m2 = fuzzy.M2(900, 2000) # Mittlere Höhe
m3 = fuzzy.M3(1400, 2000) # Große Höhe
input_sets = [m1, m2, m3]

a1 = fuzzy.M1(12, 65) # Viel Bremskraft
a2 = fuzzy.M2(30, 90) # Mittlere Bremskraft
a3 = fuzzy.M3(60, 70) # Wenig Bremskraft
output_sets = [a1, a2, a3]

agg = fuzzy.Aggregator(input_sets, [a1, a2, a3], output_upper_bound=100)
# x_val = 1200 # 200, 800, 1200, 1800
# (xx, yy), (inf1, inf2, inf3) = agg.aggregate(x_val)


# Plotten der Eingabe- und Ausgabemengen vorbereiten
input_sets_x = [[] for _ in input_sets]
input_sets_y = [[] for _ in input_sets]
output_sets_x = [[] for _ in input_sets]
output_sets_y = [[] for _ in input_sets]

for i in range(0, 2000+1):
    # Eingabemengen
    for j in range(0, len(input_sets)):
        input_sets_x[j].append(i)
        input_sets_y[j].append(input_sets[j](i))

for i in range(0, 100):
    # Ausgabemengen
    for j in range(0, len(output_sets)):
        output_sets_x[j].append(i)
        output_sets_y[j].append(output_sets[j](i))

plt.ion()
fig, (axis1, axis2) = plt.subplots(1, 2)

colors = ["red", "blue", "green"]

for x_val in range(2000, -1, -10):
    #x_val = 1200 # 200, 800, 1200, 1800
    (xx, yy), infs = agg.aggregate(x_val)

    axis1.clear()
    axis1.set_title("Eingabemengen")
    axis1.vlines(x_val, 0, max(infs), color="dimgray", linestyle="dotted")
    for i in range(0, len(input_sets)):
        axis1.plot(input_sets_x[i], input_sets_y[i], color=colors[i])
        axis1.hlines(infs[i], x_val, 2000, color=colors[i], linestyle="dotted")

    axis2.clear()
    axis2.set_title("Ausgabemengen")
    for i in range(0, len(input_sets)):
        axis2.plot(output_sets_x[i], output_sets_y[i], color=colors[i])
        axis2.hlines(infs[i], 0, 100, color=colors[i], linestyle="dotted")

    axis2.axes.get_yaxis().set_ticks([])
    plt.subplots_adjust(wspace=0.01)

    # Aggregation darstellen
    axis2.plot(xx, yy, color="black", linewidth=2)
    axis2.fill_between(xx, yy, color="gainsboro")
    # Schwerpunkt bestimmen
    centroid = fuzzy.Defuzzy().centroid(xx, yy)
    axis2.vlines(centroid, 0, 1, color="dimgray", linestyle="dashed")
    axis2.text(centroid, -0.03, f"{centroid:.1f}")
    fig.canvas.draw()
    plt.pause(0.02)

plt.ioff()
plt.show()