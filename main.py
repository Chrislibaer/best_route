from dist_function import get_multiple_distances_parallel
from genetic_functions import genetic_solution, score
from nearest_neighbor_functions import nearest_neighbor_solution
import sys


def main(cities, start):
    dists = get_multiple_distances_parallel(cities, cores=8)

    steps = 100 + len(cities) * 100

    sol, hist = genetic_solution(start, cities, dists, steps)

    url = "https://www.google.de/maps/dir/"
    for s in sol:
        url += s + "/"
    print("Result from genetic algorithm")
    print(url)
    print(score(sol, dists))

    nn_sol = nearest_neighbor_solution(cities, dists, start)
    nn_url = "https://www.google.de/maps/dir/"
    for s in nn_sol:
        nn_url += s + "/"

    print("Result from nearest neighbor algorithm")
    print(nn_url)
    print(score(nn_sol, dists))


if __name__ == '__main__':
    cities = []
    for city in sys.argv[1:]:
        cities.append(city)
    start = cities[0]

    main(cities, start)
