import matplotlib.pyplot as plt
import matplotlib.collections as mc
import random
import time
from random import uniform as ru
import math
import _graph
import _pathfinding
import _packing
from _pathfinding import euclidian_dist as euc

random.seed(0)

#######################################################

# Solves Travelling Salesman Problem solution using Ant Colony Optimization
# There are multiple couriers and packages, each courier can carry multiple packages at once 
# Each courier has its own speed, salary, max dimensions and max weight for packages
# The algorithm optimizes total cost of delivery

#######################################################


# 0. functions and classes
def money_spent(city, x, y, start, deliveries, couriers, debug = False):
    expenses = 0
    packages_per_trip = [None] * len(deliveries)

    for i in range(len(deliveries)):
        packages_per_trip[i] = []
        packages_so_far = 0

        delivery = deliveries[i]
        weight_left = couriers[i].max_weight
        packed_boxes = []
        last_point = start
        for [v, package] in delivery:
            if weight_left < package.weight or not _packing.boxes_fit(couriers[i].dimensions, packed_boxes + [package.dimensions]):
                packages_per_trip[i].append(packages_so_far)
                packages_so_far = 0

                length = _pathfinding.length(city, x, y, last_point, start)
                last_point = start
                weight_left = couriers[i].max_weight
                packed_boxes = []
                expenses += length * couriers[i].per_hour / couriers[i].speed

            packages_so_far += 1

            length = _pathfinding.length(city, x, y, last_point, v) + 2*euc(x[v], y[v], package.destination[0], package.destination[1])
            last_point = v
            weight_left -= package.weight
            packed_boxes.append(package.dimensions)
            expenses += length * couriers[i].per_hour / couriers[i].speed
        packages_per_trip[i].append(packages_so_far)

        if last_point != start:
            length = _pathfinding.length(city, x, y, last_point, start)
            expenses += length * couriers[i].per_hour / couriers[i].speed

    return [expenses, packages_per_trip]

class Courier:
    def __init__(self, speed, max_weight, dimensions, per_hour):
        self.speed = speed
        self.max_weight = max_weight
        self.dimensions = dimensions
        self.per_hour = per_hour
    def __str__(self):
        return "Швидкість: %.2f |" % self.speed + " Максимальна вага: %.2f |" % self.max_weight + " Максимальні габарити: " + " ".join(["%.2f " % i for i in self.dimensions]) + "| Годинні витрати: %.2f |" % self.per_hour

class Package:
    def __init__(self, weight, dimensions, destination, arrival_time):
        self.weight = weight
        self.dimensions = dimensions
        self.destination = destination
        self.arrival_time = arrival_time
    def __str__(self):
        return "Вага: %.2f |" % self.weight + " Габарити: " + " ".join(["%.2f " % i for i in self.dimensions]) + " | Точка доставки: " + " ".join(["%.2f " % i for i in self.destination])

# 1. generate graph
[x_lim, y_lim] = [100, 100]
[x,y,city,lines] = _graph.generate_graph(20, 20, 5, 20, x_lim, y_lim, 3, False)
city_vertices = len(city)

# 2. generate starting point
while True:
    start_i = random.randint(0, city_vertices-1)
    if 0.3 * x_lim < x[start_i] < 0.7 * x_lim and 0.3 * y_lim < y[start_i] < 0.7 * y_lim:
        break

# 3. generate packages
packages = []
package_amount = 20
for i in range(package_amount):
    case = random.random()
    if case < 0.7:
        packages.append(Package(ru(0.5, 1.5), [ru(0.1, 0.5) for i in range(3)], [ru(0, x_lim), ru(0, y_lim)], ru(9, 18)))
    elif case >= 0.7:
        packages.append(Package(ru(5, 25), [ru(0.4, 1.5) for i in range(3)], [ru(0, x_lim), ru(0, y_lim)], ru(9, 18)))

# 4. find best vertex for each package
package_indices = {}
for i in range(package_amount):
    best = None
    best_i = None
    for j in range(city_vertices):
        if j == start_i:
            continue
        dist = euc(packages[i].destination[0], packages[i].destination[1], x[j], y[j])
        if best == None or best > dist:
            best = dist
            best_i = j
    if best_i in package_indices.keys():
        package_indices[best_i].append(packages[i])
    else:
        package_indices[best_i] = [packages[i]]

# 5. generate couriers
couriers = []
couriers.append(Courier(10, 20, [1, 0.5, 1], 10000/180))
couriers.append(Courier(8, 20, [1, 0.5, 1], 9000/180))
couriers.append(Courier(15, 20, [1, 0.5, 1], 12000/180))
couriers.append(Courier(10, 20, [1, 0.5, 1], 11000/180))
couriers.append(Courier(10, 20, [1, 0.5, 1], 10000/180))

couriers.append(Courier(50, 200, [3, 4, 2], 90000/180))
couriers.append(Courier(50, 60, [2, 1, 2], 60000/180))
couriers.append(Courier(40, 200, [3, 4, 2], 80000/180))

# 6. plot graph
lc = mc.LineCollection(list(set([tuple(sorted(line)) for line in lines])), linewidths=2, linestyles="dotted")
fig, ax = plt.subplots()
ax.plot(x, y, "ob")
path_plot, = ax.plot(x[start_i], y[start_i], "r")
ax.add_collection(lc)
ax.plot(x[start_i], y[start_i], "or")
ax.plot([x[i] for i in range(city_vertices) if i in package_indices.keys()], [y[i] for i in range(city_vertices) if i in package_indices.keys()], "ok")
ax.plot([packages[i].destination[0] for i in range(package_amount)], [packages[i].destination[1] for i in range(package_amount)], "og")
plt.ion()
plt.show()

###############################################################

# 7. initialize algorithm
pv_pair = []
for key in package_indices.keys():
    for pack in package_indices[key]:
        pv_pair.append([key, pack])

ti_n = len(pv_pair)
ci_n = len(couriers)
n = ti_n + ci_n

g = [None] * n
for i in range(n):
    g[i] = [None] * n
    for j in range(n):
        p1 = [x[start_i], y[start_i]] if i >= ti_n else pv_pair[i][1].destination
        p2 = [x[start_i], y[start_i]] if j >= ti_n else pv_pair[j][1].destination
        g[i][j] = [max(euc(p1[0], p1[1], p2[0], p2[1]), 1), 1]
    g[i][i] = [0, 1]
for i in range(ti_n, n):
    for j in range(ti_n, n):
        if i != j:
            g[i][j] = [100, 1]

start = ti_n
ants = 50
best_amount = 10

a = 1
b = 1
r = 0.2

all_time_best = 100000000
all_time_best_path = None

iters = 0
plot_update_period = 1
last_update = 0

# 8. main loop (best: 4709)
while True:
    paths = []

    # find a path for each ant
    for ant in range(ants):
        path = [start]
        visited = [start]

        # 8-1. construct path
        while len(visited) < n:
            i = path[-1]
            if len(path) < 2*n: # default procedure
                p_values = [(g[i][j][1]**a) * (1/g[i][j][0]**b) if g[i][j][0] != 0 else 0 for j in range(n)]
            else: # if path is too long help terminate it
                p_values = [(g[i][j][1]**a) * (1/g[i][j][0]**b) if (g[i][j][0] != 0 and j not in visited) else 0 for j in range(n)]

            rand = random.uniform(0, sum(p_values))
            s = 0
            c = n - 1
            for j in range(n):
                s += p_values[j]
                if s > rand:
                    c = j
                    break

            path.append(c)
            if c not in visited:
                visited.append(c)

        # 8-2. get rid of duplicates
        visited = []
        i = 0
        while i < len(path) - 2:
            visited.append(path[i])
            j = i + 1
            while j < len(path):
                if path[i] == path[j]:
                    k = i + 1
                    while k <= j and k < len(path) - 1:
                        if path[k] in visited:
                            path.pop(k)
                            j -= 1
                        else:
                            k += 1
                j += 1
            i += 1

        # 8-3. translate path into deliveries
        deliveries = [None] * ci_n
        for i in path:
            if i >= ti_n:
                deliveries[i-ti_n] = []
                last_courier = i-ti_n
            else:
                deliveries[last_courier].append(pv_pair[i])
        # check whether every courier can deliver their packages
        for i in range(ci_n):
            j = 0
            while j < len(deliveries[i]):
                pv = deliveries[i][j]
                if pv[1].weight > couriers[i].max_weight or not _packing.boxes_fit(couriers[i].dimensions, [pv[1].dimensions]):
                    deliveries[i].pop(j)
                    while True:
                        rand_courier = random.randint(0, ci_n-1)
                        if couriers[rand_courier].max_weight >= pv[1].weight and _packing.boxes_fit(couriers[rand_courier].dimensions, [pv[1].dimensions]):
                            break
                    deliveries[rand_courier].append(pv)
                else:
                    j += 1

        [l, packages_per_trip] = money_spent(city, x, y, start_i, deliveries, couriers)
        # correct path
        path = []
        for i in range(ci_n):
            path.append(i+ti_n)
            packages_so_far = 0
            for pv in deliveries[i]:
                packages_so_far += 1
                path.append(pv_pair.index(pv))
                if packages_so_far >= packages_per_trip[i][0]:
                    path.append(i+ti_n)
                    packages_per_trip[i].pop(0)
                    packages_so_far = 0

        paths.append([l, path])

    paths.sort()

    if all_time_best > paths[0][0]:
        all_time_best = paths[0][0]
        all_time_best_path = paths[0][1]
        print("#######################################################################")
        for i in range(len(all_time_best_path)):
            if all_time_best_path[i] >= ti_n and i < n - 1 and all_time_best_path[i+1] < ti_n:
                print()
                print("Кур'єр " + str(all_time_best_path[i]-ti_n+1) + ":")
                print(couriers[all_time_best_path[i]-ti_n])
            elif all_time_best_path[i] < ti_n:
                print("Відправлення " + str(all_time_best_path[i]+1))
                print(pv_pair[all_time_best_path[i]][1])
        print("Витрати:", all_time_best)

    if time.time() - last_update > plot_update_period:
        x_plot = [x[pv_pair[i][0]] if i < ti_n else x[start_i] for i in all_time_best_path]
        y_plot = [y[pv_pair[i][0]] if i < ti_n else y[start_i] for i in all_time_best_path]
        path_plot.set_data(x_plot, y_plot)

        plt.title(str(all_time_best) + " / " + str(paths[0][0]))
        plt.pause(0.01)

        last_update = time.time()

    # 8-5. change the feromone amounts
    for i in range(n):
        for j in range(n):
            if i != j:
                g[i][j][1] = g[i][j][1] * (1 - r)

    for i in range(best_amount):
        for j in range(len(paths[i][1])-1):
            fi = paths[i][1][j]
            si = paths[i][1][j+1]

            to_add = r*(all_time_best/paths[i][0])**40
            g[fi][si][1] += to_add
            g[si][fi][1] += to_add

    iters += 1