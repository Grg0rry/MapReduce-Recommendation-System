#!/usr/bin/env python3

import sys
# from itertools import combinations
# import numpy as np

Movie_Vector = {}
Magnitude = {}

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    Vector = [int(item.strip()) for item in line[1].strip('[]').split(',')]
    # Vector = np.array([int(item.strip()) for item in line[1].strip('[]').split(',')])

    Movie_Vector[MovieTitle] = Vector
    # Magnitude[MovieTitle] = np.linalg.norm(Vector)

    magnitude = 0
    for val in Vector:
        magnitude += val * val
    Magnitude[MovieTitle] = magnitude


for MovieTitle_1, Vector_1 in Movie_Vector.items():
    for MovieTitle_2, Vector_2 in Movie_Vector.items():
        if MovieTitle_1 != MovieTitle_2:

            dot_product = 0
            for i in range(len(Vector_1)):
                dot_product += Vector_1[i] * Vector_2[i]
            
            similarity = dot_product / (Magnitude[MovieTitle_1] * Magnitude[MovieTitle_2])
            print('%s\t%s' % ((MovieTitle_1, MovieTitle_2), similarity))

# for (MovieTitle, Vector), (Next_MovieTitle, Next_Vector) in combinations(Movie_Vector.items(), 2):
#     dot_product = np.dot(Vector, Next_Vector)
#     similarity = dot_product / (Magnitude[MovieTitle] * Magnitude[Next_MovieTitle])
#     print('%s\t%s' % ((MovieTitle, Next_MovieTitle), similarity))
