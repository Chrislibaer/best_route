def nearest_neighbor_solution(citys, dists, start):
    solution = [start]
    available = [i for i in citys if i != start]
    current = start
    while len(available) > 0:
        distances = [[i, dists[current + '-' + i]] for i in available]
        distances.sort(key=lambda tup: tup[1])
        closest = distances[0]
        available = [i for i in available if i != closest[0]]
        current = closest[0]
        solution += [closest[0]]

    solution += [start]

    return solution