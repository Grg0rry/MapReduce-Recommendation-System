#!/usr/bin/env python3

import sys
import math
from itertools import combinations

Movie_Vector = {}
Magnitude = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = [int(item.strip()) for item in line[1].strip('[]').split(',')]

    Movie_Vector[MovieTitle] = Vector
    Magnitude[MovieTitle] = math.sqrt(sum(x ** 2 for x in Vector))

for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
    dot_product = sum(x * y for x, y in zip(Vector, Next_Vector))
    similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])

    print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))