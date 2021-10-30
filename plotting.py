import argparse
import matplotlib.pyplot as plt

import fuzzy

def init_fuzzy_system():
    m1 = fuzzy.M1(800, 1400) # Geringe Höhe
    m2 = fuzzy.M2(900, 2000) # Mittlere Höhe
    m3 = fuzzy.M3(1400, 2000) # Große Höhe
    input_sets = [m1, m2, m3]

    a1 = fuzzy.M1(12, 65) # Viel Bremskraft
    a2 = fuzzy.M2(30, 90) # Mittlere Bremskraft
    a3 = fuzzy.M3(60, 70) # Wenig Bremskraft
    output_sets = [a1, a2, a3]

    agg = fuzzy.Aggregator(input_sets, output_sets, output_upper_bound=100)
    return (input_sets, output_sets), agg


# Plotten der Eingabe- und Ausgabemengen vorbereiten
def init_set_values(input_sets, output_sets):
    input_sets_x = [[] for _ in input_sets]
    input_sets_y = [[] for _ in input_sets]
    output_sets_x = [[] for _ in input_sets]
    output_sets_y = [[] for _ in input_sets]

    # Eingabemengen
    for i in range(0, 2000+1):
        for j in range(0, len(input_sets)):
            input_sets_x[j].append(i)
            input_sets_y[j].append(input_sets[j](i))

    # Ausgabemengen
    for i in range(0, 100+1):
        for j in range(0, len(output_sets)):
            output_sets_x[j].append(i)
            output_sets_y[j].append(output_sets[j](i))

    return (input_sets_x, input_sets_y), (output_sets_x, output_sets_y)    


def plot_all(axis1, axis2, input_sets_x, input_sets_y, output_sets_x, output_sets_y, agg_x, agg_y, infs, x_val, centroid):
    colors = ["red", "blue", "green"]
    # Eingabemengen darstellen
    axis1.clear()
    axis1.set_title("Eingabemengen")
    axis1.vlines(x_val, 0, max(infs), color="dimgray", linestyle="dotted")
    for i in range(0, len(input_sets_x)):
        axis1.plot(input_sets_x[i], input_sets_y[i], color=colors[i])
        axis1.hlines(infs[i], x_val, 2000, color=colors[i], linestyle="dotted")

    # Eingabemengen darstellen
    axis2.clear()
    axis2.set_title("Ausgabemengen")
    for i in range(0, len(output_sets_x)):
        axis2.plot(output_sets_x[i], output_sets_y[i], color=colors[i])
        axis2.hlines(infs[i], 0, 100, color=colors[i], linestyle="dotted")

    axis2.axes.get_yaxis().set_ticks([])

    # Aggregation darstellen
    axis2.plot(agg_x, agg_y, color="black", linewidth=2)
    axis2.fill_between(agg_x, agg_y, color="gainsboro")
    # Schwerpunkt darstellen
    axis2.vlines(centroid, 0, 1, color="dimgray", linestyle="dashed")
    axis2.text(centroid, -0.03, f"{centroid:.1f}")


def show_animation(fig, axis1, axis2):
    plt.ion()
    
    (input_sets, output_sets), agg = init_fuzzy_system()
    (input_sets_x, input_sets_y), (output_sets_x, output_sets_y) = init_set_values(input_sets, output_sets)
    for x_val in range(2000, -1, -10):
        (agg_x, agg_y), infs = agg.aggregate(x_val)
        centroid = fuzzy.Defuzzy().centroid(agg_x, agg_y)

        plot_all(axis1, axis2, input_sets_x, input_sets_y, output_sets_x, output_sets_y, agg_x, agg_y, infs, x_val, centroid)
        
        fig.canvas.draw()
        plt.pause(0.1)

    plt.ioff()
    plt.show()


# Für eine Value (Höhe) plotten.
# Interessant: 200, 800, 1200, 1800
def show_single_value(axis1, axis2, x_val):
    (input_sets, output_sets), agg = init_fuzzy_system()
    (agg_x, agg_y), infs = agg.aggregate(x_val)
    centroid = fuzzy.Defuzzy().centroid(agg_x, agg_y)

    (input_sets_x, input_sets_y), (output_sets_x, output_sets_y) = init_set_values(input_sets, output_sets)
    plot_all(axis1, axis2, input_sets_x, input_sets_y, output_sets_x, output_sets_y, agg_x, agg_y, infs, x_val, centroid)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--value', type=int, required=False)
    args = parser.parse_args()

    fig, (axis1, axis2) = plt.subplots(1, 2)
    plt.subplots_adjust(wspace=0.01)

    if args.value: 
        show_single_value(axis1, axis2, args.value)
    else:
        show_animation(fig, axis1, axis2)