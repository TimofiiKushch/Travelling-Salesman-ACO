import math
import heapq

def euclidian_dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def length(g, x, y, i, j):
    forward_l = [None] * len(g)
    backward_l = [None] * len(g)
    forward_l[i] = 0
    backward_l[j] = 0

    forward_explored = [False] * len(g)
    backward_explored = [False] * len(g)
    forward_q = [[0, i]]
    heapq.heapify(forward_q)
    backward_q = [[0, j]]
    heapq.heapify(backward_q)

    while True:
        cf = heapq.heappop(forward_q)[1]
        forward_explored[cf] = True
        for neib in g[cf]:
            if forward_l[neib] == None:
                forward_l[neib] = forward_l[cf] + euclidian_dist(x[cf], y[cf], x[neib], y[neib])
                heapq.heappush(forward_q, [forward_l[neib], neib])
            elif forward_l[neib] > forward_l[cf] + euclidian_dist(x[cf], y[cf], x[neib], y[neib]):
                forward_l[neib] = forward_l[cf] + euclidian_dist(x[cf], y[cf], x[neib], y[neib])

        cb = heapq.heappop(backward_q)[1]
        backward_explored[cb] = True
        for neib in g[cb]:
            if backward_l[neib] == None:
                backward_l[neib] = backward_l[cb] + euclidian_dist(x[cb], y[cb], x[neib], y[neib])
                heapq.heappush(backward_q, [backward_l[neib], neib])
            elif backward_l[neib] > backward_l[cb] + euclidian_dist(x[cb], y[cb], x[neib], y[neib]):
                backward_l[neib] = backward_l[cb] + euclidian_dist(x[cb], y[cb], x[neib], y[neib])

        cf_return = forward_explored[cf] and backward_explored[cf]
        cb_return = forward_explored[cb] and backward_explored[cb]
        if cf_return or cb_return:
            if cf_return and cb_return:
                return min(forward_l[cf] + backward_l[cf], forward_l[cb] + backward_l[cb])
            elif cf_return:
                return forward_l[cf] + backward_l[cf]
            elif cb_return:
                return forward_l[cb] + backward_l[cb]


        