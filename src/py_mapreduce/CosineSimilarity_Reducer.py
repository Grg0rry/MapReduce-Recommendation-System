#!/usr/bin/env python3

import sys
from itertools import combinations
import numpy as np

Movie_Vector = {}
Magnitude = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = np.array([int(item.strip()) for item in line[1].strip('[]').split(',')])

    Movie_Vector[MovieTitle] = Vector
    Magnitude[MovieTitle] = np.linalg.norm(Vector)

    print('%s\t%s' % (MovieTitle, Magnitude[MovieTitle]))


for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
    dot_product = np.dot(Vector, Next_Vector)
    similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])
    print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))