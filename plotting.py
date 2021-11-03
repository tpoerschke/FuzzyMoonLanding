import argparse
import matplotlib.pyplot as plt

import fuzzy, library

# Globals
fig, (axis1, axis2) = plt.subplots(1, 2)
plt.subplots_adjust(wspace=0.01)

def _init_fuzzy_system(sets_type):
    input_sets, output_sets = library.load_sets(sets_type)
    agg = fuzzy.Aggregator(input_sets, output_sets, output_upper_bound=100)
    return (input_sets, output_sets), agg


# Plotten der Eingabe- und Ausgabemengen vorbereiten
def _init_set_values(input_sets, output_sets):
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


def _plot_all(input_sets_x, input_sets_y, output_sets_x, output_sets_y, agg_x, agg_y, infs, x_val, centroid):
    colors = ["tab:red", "tab:blue", "tab:green", "tab:purple", "tab:orange"]
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


def show_animation(sets_type):
    plt.ion()
    
    (input_sets, output_sets), agg = _init_fuzzy_system(sets_type)
    (input_sets_x, input_sets_y), (output_sets_x, output_sets_y) = _init_set_values(input_sets, output_sets)
    for x_val in range(2000, -1, -10):
        (agg_x, agg_y), infs = agg.aggregate(x_val)
        centroid = fuzzy.Defuzzy().centroid(agg_x, agg_y)

        _plot_all(input_sets_x, input_sets_y, output_sets_x, output_sets_y, agg_x, agg_y, infs, x_val, centroid)
        
        fig.canvas.draw()
        plt.pause(0.1)

    plt.ioff()
    plt.show()


# Für eine Value (Höhe) plotten.
# Interessant: 200, 800, 1200, 1800
def show_single_value(x_val, sets_type):
    (input_sets, output_sets), agg = _init_fuzzy_system(sets_type)
    (agg_x, agg_y), infs = agg.aggregate(x_val)
    centroid = fuzzy.Defuzzy().centroid(agg_x, agg_y)

    (input_sets_x, input_sets_y), (output_sets_x, output_sets_y) = _init_set_values(input_sets, output_sets)
    _plot_all(input_sets_x, input_sets_y, output_sets_x, output_sets_y, agg_x, agg_y, infs, x_val, centroid)
    plt.show()


# Wird verwendet, um die Mengen während
# des Spiels zu plotten... leider ineffizient
class Plotting:
    def __init__(self, input_sets, output_sets, agg, defuzzy):
        (self.input_sets_x, self.input_sets_y), (self.output_sets_x, self.output_sets_y) = _init_set_values(input_sets, output_sets)
        self.agg = agg
        self.defuzzy = defuzzy
        plt.ion()

    def update(self, x_val):
        (agg_x, agg_y), infs = self.agg.aggregate(x_val)
        centroid = self.defuzzy.centroid(agg_x, agg_y)
        _plot_all(self.input_sets_x, self.input_sets_y, self.output_sets_x, self.output_sets_y, agg_x, agg_y, infs, x_val, centroid)
        fig.canvas.draw_idle()
        plt.pause(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualisiert die Fuzzy-Mengen, deren Aggregation und Ausgabe während der Landung.")
    parser.add_argument('--value', type=int, required=False, help="Plottet einen einzigen X-Wert (hier Höhe) und spielt keine Animation ab.")
    parser.add_argument('--variant', type=str, required=False, default=library.SETS3, choices=library.ALL_VARIANTS, help="Verwendet die gewählte Konfiguration an Fuzzy-Mengen.")
    args = parser.parse_args()

    if args.value: 
        show_single_value(args.value, args.variant)
    else:
        show_animation(args.variant)