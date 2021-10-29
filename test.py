import fuzzy

import matplotlib.pyplot as plt

m1 = fuzzy.M1(300, 1000)
m2 = fuzzy.M2(500, 1500)
m3 = fuzzy.M3(1000, 1700)

a1 = fuzzy.M1(20, 50)
a2 = fuzzy.M2(25, 75)
a3 = fuzzy.M3(50, 80)

agg = fuzzy.Aggregator([m1, m2, m3], [a1, a2, a3], 100)
x_val = 1200
(xx, yy), (inf1, inf2, inf3) = agg.aggregate(x_val)


# Eingabe- und Ausgabemengen plotten
mx1, my1 = [], []
mx2, my2 = [], []
mx3, my3 = [], []
ax1, ay1 = [], []
ax2, ay2 = [], []
ax3, ay3 = [], []

fig, (axis1, axis2) = plt.subplots(1, 2)

for i in range(0, 2000+1):
    # Eingabemengen
    mx1.append(i)
    my1.append(m1(i))
    mx2.append(i)
    my2.append(m2(i))
    mx3.append(i)
    my3.append(m3(i))

for i in range(0, 100):
     # Ausgabemengen
    ax1.append(i)
    ay1.append(a1(i))
    ax2.append(i)
    ay2.append(a2(i))
    ax3.append(i)
    ay3.append(a3(i))


axis1.set_title("Eingabemengen")
axis1.vlines(x_val, 0, max(inf1, inf2, inf3), color="gray", linestyle="dotted")
axis1.plot(mx1, my1, color="red")
axis1.hlines(inf1, x_val, 2000, color="red", linestyle="dotted")
axis1.plot(mx2, my2, color="blue")
axis1.hlines(inf2, x_val, 2000, color="blue", linestyle="dotted")
axis1.plot(mx3, my3, color="green")
axis1.hlines(inf3, x_val, 2000, color="green", linestyle="dotted")

axis2.set_title("Ausgabemengen")
axis2.plot(ax1, ay1, color="red")
axis2.hlines(inf1, 0, 100, color="red", linestyle="dotted")
axis2.plot(ax2, ay2, color="blue")
axis2.hlines(inf2, 0, 100, color="blue", linestyle="dotted")
axis2.plot(ax3, ay3, color="green")
axis2.hlines(inf3, 0, 100, color="green", linestyle="dotted")

# Aggregation darstellen
axis2.plot(xx, yy, color="black", linewidth="2")
axis2.axes.get_yaxis().set_ticks([])

# Schwerpunkt bestimmen
centroid = fuzzy.Defuzzy().centroid(xx, yy)
axis2.vlines(centroid, 0, 1, color="gray", linestyle="dashed")

plt.subplots_adjust(wspace=0.05)
plt.show()

