'''
    Algoritmul care construieste in context euclidian un traseu optim pentru TSP
    folosind acoperirea convexa
    TSP: graf ponderat neorientat complet
    Sursa AA: https://github.com/DimaOanaTeodora/Advanced-Algorithms-Course
'''
from math import sqrt

f = open("TSP_input.txt")
points = []
n = int(f.readline())
for i in range(n):
    line = f.readline()
    v = line.split()
    x = int(v[0])
    y = int(v[1])
    points.append((x, y))


def det(points):
    # calculez determinantul pt o lista points alcatuita din 3 puncte
    det = points[1][0] * points[2][1] + points[2][0] * points[0][1] + points[0][0] * points[1][1] - points[0][1] * \
          points[1][0] - points[0][0] * points[2][1] - points[1][1] * points[2][0]

    return det

# calculez acoperirea convexa
points = sorted(points)
Li = []
for p in points:
    while len(Li) >= 2 and det([Li[-2], Li[-1], p]) <= 0:
        Li.pop(-1)
    Li.append(p)
Li.pop(-1)

points.reverse()
Ls = []
for p in points:
    while len(Ls) >= 2 and det([Ls[-2], Ls[-1], p]) <= 0:
        Ls.pop(-1)
    Ls.append(p)
Ls.pop(-1)

P = Li + Ls  # concatenare
print("Li: ", Li)
print("Ls: ", Ls)

def DE(p1, p2):
    #distanta euclidiana
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def d1(point, pos, P):
    return DE(P[pos], point) + DE(point, P[(pos + 1) % len(P)]) / DE(P[pos], P[(pos + 1) % len(P)])


def d2(point, pos, P):
    return DE(P[pos], point) + DE(point, P[(pos + 1) % len(P)]) - DE(P[pos], P[(pos + 1) % len(P)])


def TSP(P, points):
    l = []  
    for p in points:
        if p not in P: #pun doar punctele care nu fac parte din Li Ls
            l.append(p)

    while len(l) > 0:
        minimum_dist = [0.0] * 3
        minimum_dist[0] = 999999

        for p in l:
            i = 0

            min_dist = 999999
            for pos in range(len(P)):
                if d1(p, pos, P) < min_dist:
                    i = pos
                    min_dist = d1(p, pos, P)

            if d2(p, i, P) < minimum_dist[0]:
                minimum_dist[2] = i
                minimum_dist[0] = d2(p, i, P)
                minimum_dist[1] = p

        l.remove(minimum_dist[1])
        P.insert(minimum_dist[2], minimum_dist[1])
    return P


output = TSP(P, points)

print(output)