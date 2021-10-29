import fuzzy

import matplotlib.pyplot as plt

m1 = fuzzy.M1(300, 1000)
m2 = fuzzy.M2(500, 1500)
m3 = fuzzy.M3(1000, 1700)

a1 = fuzzy.M1(20, 50)
a2 = fuzzy.M2(25, 75)
a3 = fuzzy.M3(50, 80)

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

x_val = 1200
infx1 = m1(x_val)
infx2 = m2(x_val)
infx3 = m3(x_val)

axis1.set_title("Eingabemengen")
axis1.plot(mx1, my1, color="red")
axis1.hlines(infx1, x_val, 2000, color="red", linestyle="dotted")
axis1.plot(mx2, my2, color="blue")
axis1.hlines(infx2, x_val, 2000, color="blue", linestyle="dotted")
axis1.plot(mx3, my3, color="green")
axis1.hlines(infx3, x_val, 2000, color="green", linestyle="dotted")

axis2.set_title("Ausgabemengen")
axis2.plot(ax1, ay1, color="red")
axis2.hlines(infx1, 0, 100, color="red", linestyle="dotted")
axis2.plot(ax2, ay2, color="blue")
axis2.hlines(infx2, 0, 100, color="blue", linestyle="dotted")
axis2.plot(ax3, ay3, color="green")
axis2.hlines(infx3, 0, 100, color="green", linestyle="dotted")

xx = []
yy = []

for i in range(0, 100):
    a1_ = min(infx1, a1(i))
    a2_ = min(infx2, a2(i))
    a3_ = min(infx3, a3(i))
    xx.append(i)
    yy.append(max(a1_, a2_, a3_))

axis2.plot(xx, yy, color="gray")

plt.show()

