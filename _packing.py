import random

# 
def boxes_fit(container, boxes):
    x_dim = [container[0]] + [box[0] for box in boxes]
    y_dim = [container[1]] + [box[1] for box in boxes]
    z_dim = [container[2]] + [box[2] for box in boxes]
    [x_dim, y_dim, z_dim] = sorted([x_dim, y_dim, z_dim], reverse=True)
    
    container = [x_dim[0], y_dim[0], z_dim[0]]
    boxes = [[x_dim[i], y_dim[i], z_dim[i]] for i in range(1,len(x_dim))]
    boxes = sorted(boxes, reverse=True) # pack in order of decreasing height

    if not (container[0] >= boxes[0][0] and container[1] >= boxes[0][1] and container[2] >= boxes[0][2]):
        return False

    packed = {(0, 0, 0) : tuple(boxes[0])}
    boxes.pop(0)
    while len(boxes) > 0:
        can_pack = False
        for pos in packed.keys():
            packed_box = packed[pos]
            pivots = [None] * 3
            for i in range(3):
                pivots[i] = list(pos)
                pivots[i][i] += packed_box[i]
            pivots.reverse() # pack from least important dimension
            for pivot in pivots:
                b = boxes[0]
                permutations = [(b[0], b[1], b[2]), (b[0], b[2], b[1]), (b[1], b[0], b[2]), (b[1], b[2], b[0]), (b[2], b[0], b[1]), (b[2], b[1], b[0])]
                permutations = list(set(permutations))

                for permut in permutations:
                    if pivot[0] + permut[0] <= container[0] and pivot[1] + permut[1] <= container[1] and pivot[2] + permut[2] <= container[2]:
                        boxes_dont_overlap = True
                        for pos1 in packed.keys():
                            e1 = pivot
                            e2 = [pivot[0] + permut[0], pivot[1] + permut[1], pivot[2] + permut[2]]
                            e3 = list(pos1)
                            e4 = [pos1[0] + packed[pos1][0], pos1[1] + packed[pos1][1], pos1[2] + packed[pos1][2]]
                            if so(e1[0], e2[0], e3[0], e4[0]) and so(e1[1], e2[1], e3[1], e4[1]) and so(e1[2], e2[2], e3[2], e4[2]):
                                boxes_dont_overlap = False
                                break
                        if boxes_dont_overlap:
                            can_pack = True
                            new_pack = [tuple(pivot), tuple(permut)]
                    if can_pack:
                        break
                if can_pack:
                    break
            if can_pack:
                break
        if can_pack:
            boxes.pop(0)
            packed[new_pack[0]] = new_pack[1]
        else:
            return False
    return True

def so(a1, b1, a2, b2):
    return a2 < b1 and a1 < b2

if __name__ == "__main__":
    container = [4, 10, 6]
    boxes = [[4, 4, 6], [2, 5, 3], [2, 2, 3], [4, 2, 3], [3, 2, 5]]
    print(boxes_fit(container, boxes))

    container = [1, 1, 1]
    boxes = [[1, 1, 1]]
    print(boxes_fit(container, boxes))

    container = [1, 1, 2]
    boxes = [[1, 1, 1], [1, 1, 1]]
    print(boxes_fit(container, boxes))

    container = [2, 2, 2]
    boxes = [[1, 1, 1], [1, 1, 1], [2, 2, 1], [1, 2, 1]]
    print(boxes_fit(container, boxes))

    container = [2, 2, 2]
    boxes = [[1, 1, 1], [1, 2, 1], [2, 2, 1], [1, 2, 1]]
    print(boxes_fit(container, boxes))