'''
    i) Alegeți ordinea de parcurgere a punctelor intermediare astfel încât să minimizați
    lungimea traiectoriei (de exemplu printr-un algoritm de tipul traveling
    salesman problem).

    Algoritmul care construieste in context euclidian un traseu optim pentru TSP
    folosind acoperirea convexa
    TSP: graf neorientat complet
'''
from math import sqrt

def det(points):
    # calculez determinantul pt o lista alcatuita din 3 puncte
    det = points[1][0] * points[2][1] + points[2][0] * points[0][1] + points[0][0] * points[1][1] - points[0][1] * \
          points[1][0] - points[0][0] * points[2][1] - points[1][1] * points[2][0]

    return det

def DE(p1, p2):
    # distanta euclidiana
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def d1(point, pos, CH):
    return DE(CH[pos], point) + DE(point, CH[(pos + 1) % len(CH)]) / DE(CH[pos], CH[(pos + 1) % len(CH)])


def d2(point, pos, CH):
    return DE(CH[pos], point) + DE(point, CH[(pos + 1) % len(CH)]) - DE(CH[pos], CH[(pos + 1) % len(CH)])

def TSP(CH, points):
    l = []  # lista de puncte care nu sunt parte din acoperirea convexa
    for p in points:
        if p not in CH: 
            l.append(p)

    while len(l) > 0:
        minimum_dist = [0.0] * 3
        minimum_dist[0] = 999999
        # pe poz 0 e distanta minima
        # pe poz 1 e punctul care nu e in CH
        # pe poz 2 e pozitia punctului care e in CH

        for p in l:
            i = 0
            min_dist = 999999
        
            for pos in range(len(CH)):
                # calculez punctul cel mai apropiat de CH 
                if d1(p, pos, CH) < min_dist:
                    i = pos
                    min_dist = d1(p, pos, CH)

            # retin distnta minima overall in minimum_dist[0]
            if d2(p, i, CH) < minimum_dist[0]:
                minimum_dist[0] = d2(p, i, CH)
                minimum_dist[1] = p
                minimum_dist[2] = i

        l.remove(minimum_dist[1]) # il scot din stiva
        CH.insert(minimum_dist[2], minimum_dist[1]) # il inserez pe pozitia i 

    return CH


points = [(1, 1), (8, 2), (4, 6), (4, 4), (2, 8), (10, 6), (8, 8)]
n = 7

# -------- calculez acoperirea convexa ------------

# calculez limita inferioara a acoperirii (Li)
points = sorted(points) # sortez in ordine crescatoare dupa x
Li = []
for p in points: # parcurg punctele in ordinea x crescator 
    while len(Li) >= 2 and det([Li[-2], Li[-1], p]) <= 0:
        # formez triunghiuri
        # determinantul triunghiurilor formate trebuie sa fie mereu > 0
        # in caz contrar, nu e bun nodul din mijloc
        Li.pop(-1)
    Li.append(p)
Li.pop(-1)

# calculez limita superioara a acoperirii
points.reverse()
Ls = []
for p in points:
    while len(Ls) >= 2 and det([Ls[-2], Ls[-1], p]) <= 0:
        Ls.pop(-1)
    Ls.append(p)
Ls.pop(-1)

print("L inferioara: ", Li)
print("L superioara: ", Ls)

# acoperirea convexa
CH = Li + Ls  # concatenarea limitelor 

print("acoperirea convexa: ", CH)
output = TSP(CH, points)

print(output)