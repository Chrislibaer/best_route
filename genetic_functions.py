import random


def score(solution, dists):
    ret = 0
    for city1, city2 in zip(solution, solution[1:]):
        ret += dists[city1 + '-' + city2]

    return ret


def generate_random_solution(citys, start):
    citys = [city for city in citys if city != start]
    random.shuffle(citys)

    return [start] + citys + [start]


def breed(parent1, parent2, start):
    parent1 = parent1[1:-1]
    parent2 = parent2[1:-1]

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    childp1 = parent1[startGene:endGene]
    childp2 = [i for i in parent2 if i not in childp1]

    ret = [start] + childp2[:startGene] + parent1[startGene:endGene] + childp2[startGene:] + [start]

    return ret


def random_breed(parent1, citys, start):
    parent1 = parent1[1:-1]
    parent2 = generate_random_solution(citys, start)[1:-1]

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    childp1 = parent1[startGene:endGene]
    childp2 = [i for i in parent2 if i not in childp1]

    ret = [start] + childp2[:startGene] + parent1[startGene:endGene] + childp2[startGene:] + [start]

    return ret


def permute(parent1, start):
    parent1 = parent1[1:-1]
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    tmp = parent1[geneA]
    parent1[geneA] = parent1[geneB]
    parent1[geneB] = tmp

    return [start] + parent1 + [start]


def multi_permute(parent1, start):
    parent1 = parent1[1:-1]

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    to_shuffle = parent1[startGene:endGene]
    random.shuffle(to_shuffle)

    parent1 = parent1[:startGene] + to_shuffle + parent1[endGene:]

    return [start] + parent1 + [start]


# similar to this paper https://www.sciencedirect.com/science/article/pii/S0377221701002272
def moon_crossover(parent1, parent2, start):
    parent1 = parent1[1:-1]
    parent2 = parent2[1:-1]

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    p1 = parent1[:startGene]
    p2 = parent1[startGene:endGene]
    p3 = [i for i in parent2 if i not in p2]

    while len(p1) > 0 or len(p3) > 0:
        if len(p1) > 0:
            if p1[-1] not in p2:
                p2 = [p1[-1]] + p2
            p1 = p1[:-1]
        if len(p3) > 0:
            if p3[0] not in p2:
                p2 = p2 + [p3[0]]
            p3 = p3[1:]

    ret = [start] + p2 + [start]

    return ret


def genetic_solution(start, citys, dists, steps):
    matingpool = [generate_random_solution(citys, start) for _ in range(100)]
    matingpool = [[i, score(i, dists)] for i in matingpool]

    best_history = []

    for _ in range(steps):
        matingpool.sort(key=lambda tup: tup[1])
        best = matingpool[0]

        # print(score(matingpool[0][0], stops))

        best_history.append(best)

        # survival of the fittest
        matingpool = matingpool[0:30]

        # reproduce
        # breeding
        breedpool = [breed(par1[0], par2[0], start) for par1, par2 in
                     zip(random.choices(matingpool, k=20), random.choices(matingpool, k=20))]

        breedpool_copy = [[i, score(i, dists)] for i in breedpool]
        breedpool_copy.sort(key=lambda tup: tup[1])

        if breedpool_copy[0][1] < best[1]:
            print("better solution through breeding!")
            breeding_fail = False
        else:
            breeding_fail = True

        matingpool += [[i, score(i, dists)] for i in breedpool]

        # moon crossover
        moonpool = [moon_crossover(par1[0], par2[0], start) for par1, par2 in
                    zip(random.choices(matingpool, k=10), random.choices(matingpool, k=10))]

        moonpool_copy = [[i, score(i, dists)] for i in moonpool]
        moonpool_copy.sort(key=lambda tup: tup[1])

        if moonpool_copy[0][1] < best[1]:
            print("better solution through moon crossover!")
            moon_fail = False
        else:
            moon_fail = True

        matingpool += [[i, score(i, dists)] for i in moonpool]

        # random breed
        random_breedpool = [random_breed(par1[0], citys, start) for par1 in random.choices(matingpool, k=10)]
        matingpool += [[i, score(i, dists)] for i in random_breedpool]

        # permute
        permute_pool = [permute(par1[0], start) for par1 in random.choices(matingpool, k=10)]

        permute_pool_copy = [[i, score(i, dists)] for i in permute_pool]
        permute_pool_copy.sort(key=lambda tup: tup[1])

        permute_pool = [[i, score(i, dists)] for i in permute_pool]

        if permute_pool_copy[0][1] < best[1]:
            print("better solution through permutation!")
            permute_fail = False
        else:
            permute_fail = True

        matingpool += permute_pool

        # multi permute
        multi_permute_pool = [multi_permute(par1[0], start) for par1 in random.choices(matingpool, k=10)]

        multi_permute_pool_copy = [[i, score(i, dists)] for i in multi_permute_pool]
        multi_permute_pool_copy.sort(key=lambda tup: tup[1])

        multi_permute_pool = [[i, score(i, dists)] for i in multi_permute_pool]

        if multi_permute_pool_copy[0][1] < best[1]:
            print("better solution through multi permutation!")
            multi_permute_fail = False
        else:
            multi_permute_fail = True

        matingpool += multi_permute_pool

        # random
        randompool = [generate_random_solution(citys, start) for _ in range(10)]

        randompool_copy = [[i, score(i, dists)] for i in randompool]
        randompool_copy.sort(key=lambda tup: tup[1])

        randompool = [[i, score(i, dists)] for i in randompool]

        if randompool_copy[0][1] < best[1]:
            print("better solution through random new solution!")
            random_fail = False
        else:
            random_fail = True

        if random_fail and breeding_fail and permute_fail and multi_permute_fail:
            print("no better solution found")

        matingpool += randompool

        # if steps % 100 == 0:
        # print(matingpool)

    return matingpool[0][0], best_history