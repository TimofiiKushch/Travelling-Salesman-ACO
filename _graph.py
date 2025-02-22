import matplotlib.pyplot as plt
import matplotlib.collections as mc
import random
import math

def euclidian_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# generates random graph
def generate_graph(rows, cols, min_dist, max_dist, x_lim, y_lim, sigma, debug = False):
    x = []
    y = []
    for i in range(rows):
        for j in range(cols):
            x.append(i*x_lim/rows + random.gauss(0, sigma))
            y.append(j*y_lim/cols + random.gauss(0, sigma))

    l = [i for i in zip(x,y)]
    i = 0
    while i < len(l):
        current = l[i]
        j = 0
        while j < len(l):
            another = l[j]
            if 0 < euclidian_dist(current, another) < min_dist:
                l.pop(j)
            else:
                j += 1
        i += 1

    n = len(l)
    g = [None] * n
    for i in range(n):
        g[i] = []

    for i in range(n):
        quad_closest = [None] * 4
        for j in range(n):
            if j == i:
                continue
            d = euclidian_dist(l[i], l[j])
            quad = int(l[i][0] > l[j][0]) * 2 + int(l[i][1] > l[j][1])
            if quad_closest[quad] == None or quad_closest[quad][0] > d:
                if d < max_dist:
                    quad_closest[quad] = [d, j]
        for quad in quad_closest:
            if quad == None:
                continue
            if quad[1] not in g[i]:
                g[i].append(quad[1])
            if i not in g[quad[1]]:
                g[quad[1]].append(i)

    lines = []
    for i in range(n):
        for j in g[i]:
            lines.append([l[i], l[j]])

    x = [i[0] for i in l]
    y = [i[1] for i in l]

    if debug:
        lc = mc.LineCollection(lines, linewidths=2)
        fig, ax = plt.subplots()
        ax.plot(x, y, "o")
        ax.add_collection(lc)

        plt.show()

    return x, y, g, lines

if __name__ == "__main__":
    generate_graph(20, 20, 5, 20, 100, 100, 3, True)